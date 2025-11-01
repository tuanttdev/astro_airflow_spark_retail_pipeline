# my_dag.py
from airflow.decorators import dag, task
from datetime import datetime

from pyspark import SparkContext
from pyspark.sql import SparkSession
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
import pandas as pd


@dag(
    start_date=datetime(2025, 8, 1),
    end_date=datetime(2025, 12, 31),
    schedule="0 0 * * *",
    max_active_runs=1,
    catchup=False,
)

def staging_dag():
    from airflow.models import Variable

    execution_date = Variable.get("current_date")

    packages = "org.postgresql:postgresql:42.7.4," \
                 "com.clickhouse:clickhouse-jdbc:0.6.1," \
                 "com.clickhouse:clickhouse-http-client:0.6.1," \

    stg_sales_transactions_job = SparkSubmitOperator(
        task_id="stg_sales_transactions_job",
        conn_id="my_spark_conn",
        application="include/script/stg_jobs.py",
        packages="org.postgresql:postgresql:42.7.4",
        application_args=["--date", execution_date, "--job", "sales_tx"],
        verbose=True,
    )

    stg_channel_performance_job= SparkSubmitOperator(
        task_id="stg_channel_performance_job",
        conn_id="my_spark_conn",
        application="include/script/stg_jobs.py",
        packages="org.postgresql:postgresql:42.7.4",
        application_args=["--date", execution_date, "--job", "channel_perf"],
        verbose=True,
    )

    load_dim_channel_job = SparkSubmitOperator(
        task_id="load_dim_channel_job",
        conn_id="my_spark_conn",
        application="include/script/warehouse_loaders.py",
        application_args=["--date", execution_date, "--job", "dim_channel"],
        packages=packages,
        verbose=True,
    )

    load_dim_product_job = SparkSubmitOperator(
        task_id="load_dim_product_job",
        conn_id="my_spark_conn",
        application="include/script/warehouse_loaders.py" ,
        application_args=["--date", execution_date, "--job", "dim_product"],
        packages=packages,
        verbose=True,
    )

    process_sales_data_to_warehouse_job = SparkSubmitOperator(
        task_id="process_sales_data_to_warehouse_job",
        conn_id="my_spark_conn",
        application="include/script/warehouse_loaders.py",
        application_args=["--date", execution_date, "--job", "fact_sale"],
        packages=packages,
        verbose=True,
    )

    stg_sales_transactions_job >> stg_channel_performance_job >> [load_dim_channel_job, load_dim_product_job] >> process_sales_data_to_warehouse_job


staging_dag()