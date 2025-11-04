from airflow.decorators import dag, task
from datetime import datetime

from pyspark import SparkContext
from pyspark.sql import SparkSession
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator



@dag(
    start_date=datetime(2025, 8, 1),

    schedule="0 0 1 * *",
    max_active_runs=1,
    max_active_tasks=4,
    catchup=False,
)

def auto_increase_date_dimension():
    # from airflow.models import Variable
    import os
    AIRFLOW_MOUNT_DIR = "/usr/local/airflow"  # Hoac /opt/airflow, tuy thuoc vao image base cua ban

    SPARK_APP_PATH_WAREHOUSE_LOADER = os.path.join(AIRFLOW_MOUNT_DIR, "include", "script", "warehouse_loaders.py")
    #### airflow dags backfill     --start-date 2025-04-29     --end-date 2025-04-30  --rerun-failed-tasks   staging_dag

    packages = "org.postgresql:postgresql:42.7.4," \
                 "com.clickhouse:clickhouse-jdbc:0.6.1," \
                 "com.clickhouse:clickhouse-http-client:0.6.1," \

    auto_increase_date_dimension_job = SparkSubmitOperator(
        task_id="auto_increase_date_dimension_job",
        conn_id="my_spark_conn",
        application=SPARK_APP_PATH_WAREHOUSE_LOADER,
        application_args=["--start_time", "{{data_interval_start}}", "--end_time", "{{ data_interval_end }}",
                          "--job", "dim_date"],
        packages=packages,
        verbose=True,
    )

    auto_increase_date_dimension_job


auto_increase_date_dimension()