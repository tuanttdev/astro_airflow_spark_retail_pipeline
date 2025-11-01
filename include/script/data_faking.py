import pandas as pd
import numpy as np
from pathlib import Path

def _safe_read_ids(csv_path: str, prefer_cols=('customer_id','store_id','employee_id','channel')):
    """Đọc 1 cột ID từ CSV. Ưu tiên các tên cột phổ biến; nếu không có thì lấy cột đầu tiên."""
    p = Path(csv_path)

    if not p.exists():
        raise FileNotFoundError(f"Không thấy file: {csv_path}")
    df = pd.read_csv(p)
    # tìm cột phù hợp
    for c in prefer_cols:
        if c in df.columns:
            col = c
            break
    else:
        col = df.columns[0]
    # loại NA, chuyển về str, bỏ trùng
    ids = df[col].dropna().astype(str).drop_duplicates().tolist()
    if not ids:
        raise ValueError(f"File {csv_path} không có giá trị hợp lệ ở cột '{col}'.")
    return ids

def gen_orders(
    n: int,
    customers_csv: str,
    stores_csv: str,
    employees_csv: str,
    channels_csv: str,
    start_date: str = "2025-01-01",
    end_date: str   = "2025-01-31",
    seed: int | None = 42,
    write_to: str | None = None,
    order_prefix: str = "ORD",
    start_seq: int = 1,
):
    """
    Sinh n đơn hàng với schema:
    order_id,order_date,customer_id,store_id,employee_id,channel,total_amount,discount_amount,final_amount,payment_method,status

    - *_csv: đường dẫn tới các file CSV có cột tương ứng:
        customers_csv  -> có cột 'customer_id' (hoặc sẽ lấy cột đầu tiên)
        stores_csv     -> 'store_id'
        employees_csv  -> 'employee_id'
        channels_csv   -> 'channel'
    - start_date/end_date: YYYY-MM-DD (bao gồm cả hai đầu)
    - write_to: nếu truyền vào, sẽ ghi ra CSV; vẫn trả về DataFrame
    - start_seq: thứ tự bắt đầu để tạo order_id (ORD001, ORD002, ...)
    """
    rng = np.random.default_rng(seed)

    customers = _safe_read_ids(customers_csv, ('customer_id',))
    stores    = _safe_read_ids(stores_csv, ('store_id',))
    employees = _safe_read_ids(employees_csv, ('employee_id',))
    channels  = _safe_read_ids(channels_csv, ('channel','sales_channel','channel_name'))

    # dải ngày
    dates = pd.date_range(start_date, end_date, freq="D")
    if len(dates) == 0:
        raise ValueError("Khoảng ngày không hợp lệ.")

    # payment methods & status
    payment_methods = np.array(["Cash", "Credit Card", "E-Wallet", "Bank Transfer"])
    payment_weights = np.array([0.25, 0.35, 0.30, 0.10])  # tổng = 1
    statuses = np.array(["Completed", "Pending", "Cancelled"])
    status_weights = np.array([0.90, 0.07, 0.03])

    # total_amount: VND, bội số 50,000 (từ 200k đến 3 triệu)
    total_min = 200_000
    total_max = 3_000_000
    step = 50_000

    # discount %: 0/5/10/15 (nặng về 0 và 10)
    discount_choices = np.array([0, 5, 10, 15])
    discount_weights = np.array([0.45, 0.15, 0.30, 0.10])

    rows = []
    for i in range(n):
        order_seq = start_seq + i
        order_id = f"{order_prefix}{order_seq:03d}"

        order_date = rng.choice(dates).date().isoformat()
        customer_id = rng.choice(customers)
        store_id = rng.choice(stores)
        employee_id = rng.choice(employees)
        channel = rng.choice(channels)

        # Tổng tiền
        total_amount = int(rng.integers(total_min // step, 1 + total_max // step) * step)

        # Giảm giá
        d_pct = rng.choice(discount_choices, p=discount_weights)
        discount_amount = int(total_amount * d_pct / 100)

        final_amount = total_amount - discount_amount

        payment_method = rng.choice(payment_methods, p=payment_weights)
        status = rng.choice(statuses, p=status_weights)

        rows.append([
            order_id, order_date, customer_id, store_id, employee_id, channel,
            total_amount, discount_amount, final_amount, payment_method, status
        ])

    df = pd.DataFrame(rows, columns=[
        "order_id","order_date","customer_id","store_id","employee_id","channel",
        "total_amount","discount_amount","final_amount","payment_method","status"
    ])

    # Một số ràng buộc nhẹ theo channel -> payment (tuỳ chọn)
    # Ví dụ: nếu channel là "Online" hoặc "Mobile App" thì ưu tiên non-cash
    online_mask = df["channel"].str.lower().isin(["online", "mobile app", "app", "web"])
    if online_mask.any():
        non_cash = ["Credit Card","E-Wallet","Bank Transfer"]
        df.loc[online_mask, "payment_method"] = rng.choice(non_cash, size=online_mask.sum())

    if write_to:
        Path(write_to).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(write_to, index=False, encoding="utf-8")

    return df

# --- Ví dụ dùng ---
df = gen_orders(
    n=5,
    customers_csv="./include/data_example/CUSTOMERS.csv",
    stores_csv="./include/data_example/STORES.csv",
    employees_csv="./include/data_example/EMPLOYEES.csv",
    channels_csv="./include/data_example/CHANNELS.csv",
    start_date="2025-01-15",
    end_date="2025-01-17",
    seed=123,
    write_to="../orders_sample.csv"
)
print(df)