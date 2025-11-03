from airflow.operators.bash import BashOperator
from airflow.models.dag import DAG
from datetime import datetime

with DAG(
        dag_id="backfill_dag",
        start_date=datetime(2025, 1, 1),
        schedule_interval="@monthly",
        # schedule="* * * * *",

        catchup=False,
) as dag:
    process_data_task = BashOperator(
        task_id="trigger_dag_run",
        bash_command="airflow dags backfill     --start-date 2025-04-15     --end-date 2025-04-30  --rerun-failed-tasks   staging_dag",
    )