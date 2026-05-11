from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import (
    SparkSubmitOperator,
)
from pendulum import datetime


with DAG(
    dag_id="compute_metrics_spark",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["lab3", "spark"],
) as dag:
    spark_job = SparkSubmitOperator(
        task_id="compute_metrics_spark_job",
        application="/opt/airflow/spark/compute_metrics_spark.py",
        conn_id="spark_local",
        name="compute_metrics_spark_job",
    )
