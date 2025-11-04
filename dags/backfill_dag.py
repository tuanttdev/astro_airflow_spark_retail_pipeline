from airflow.operators.bash import BashOperator
from airflow.models.dag import DAG
from datetime import datetime

with DAG(
        dag_id="backfill_dag",
        start_date=datetime(2025, 1, 1),
        # schedule_interval="@monthly",
        schedule="0 0 1 * *",

        catchup=False,
) as dag:
    process_data_task = BashOperator(
        task_id="trigger_dag_run",
        bash_command="airflow dags backfill     --start-date {{data_interval_start}}     --end-date {{data_interval_end}}  --rerun-failed-tasks   etl_sale_data",
    )