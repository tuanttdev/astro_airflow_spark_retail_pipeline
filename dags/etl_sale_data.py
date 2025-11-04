from airflow.decorators import dag, task
from datetime import datetime

from pyspark import SparkContext
from pyspark.sql import SparkSession
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator



@dag(
    start_date=datetime(2025, 8, 1),
    end_date=datetime(2025, 12, 31),
    schedule="0 0 * * *",
    max_active_runs=1,
    max_active_tasks=4,
    catchup=False,
)

def etl_sale_data():
    # from airflow.models import Variable
    import os
    AIRFLOW_MOUNT_DIR = "/usr/local/airflow"  # Hoac /opt/airflow, tuy thuoc vao image base cua ban

    SPARK_APP_PATH_STAGING_JOB = os.path.join(AIRFLOW_MOUNT_DIR, "include", "script", "stg_jobs.py")

    SPARK_APP_PATH_WAREHOUSE_LOADER = os.path.join(AIRFLOW_MOUNT_DIR, "include", "script", "warehouse_loaders.py")
    #### airflow dags backfill     --start-date 2025-04-29     --end-date 2025-04-30  --rerun-failed-tasks   staging_dag

    packages = "org.postgresql:postgresql:42.7.4," \
                 "com.clickhouse:clickhouse-jdbc:0.6.1," \
                 "com.clickhouse:clickhouse-http-client:0.6.1," \


    stg_sales_transactions_job = SparkSubmitOperator(
        task_id="stg_sales_transactions_job",
        conn_id="my_spark_conn",
        # application="include/script/stg_jobs.py",
        application = SPARK_APP_PATH_STAGING_JOB,
        packages="org.postgresql:postgresql:42.7.4",
        application_args=["--start_time", "{{ data_interval_start }}", "--end_time", "{{ data_interval_end }}", "--job", "sales_tx"],
        verbose=True,
    )

    stg_channel_performance_job= SparkSubmitOperator(
        task_id="stg_channel_performance_job",
        conn_id="my_spark_conn",
        application=SPARK_APP_PATH_STAGING_JOB,
        packages="org.postgresql:postgresql:42.7.4",
        application_args=["--start_time", "{{data_interval_start}}", "--end_time", "{{ data_interval_end }}",
                          "--job", "channel_perf"],
        verbose=True,
    )

    load_dim_channel_job = SparkSubmitOperator(
        task_id="load_dim_channel_job",
        conn_id="my_spark_conn",
        application=SPARK_APP_PATH_WAREHOUSE_LOADER,
        application_args=["--start_time", "{{data_interval_start}}", "--end_time", "{{ data_interval_end }}",
                          "--job", "dim_channel"],
        packages=packages,
        verbose=True,
    )

    load_dim_product_job = SparkSubmitOperator(
        task_id="load_dim_product_job",
        conn_id="my_spark_conn",
        application=SPARK_APP_PATH_WAREHOUSE_LOADER ,
        application_args=["--start_time", "{{data_interval_start}}", "--end_time", "{{ data_interval_end }}",
                          "--job", "dim_product"],
        packages=packages,
        verbose=True,
    )

    process_sales_data_to_warehouse_job = SparkSubmitOperator(
        task_id="process_sales_data_to_warehouse_job",
        conn_id="my_spark_conn",
        application=SPARK_APP_PATH_WAREHOUSE_LOADER,
        application_args=["--start_time", "{{data_interval_start}}", "--end_time", "{{ data_interval_end }}",
                          "--job", "fact_sale"],
        packages=packages,
        verbose=True,
    )

    stg_sales_transactions_job >> stg_channel_performance_job >> [load_dim_channel_job, load_dim_product_job] >> process_sales_data_to_warehouse_job


etl_sale_data()