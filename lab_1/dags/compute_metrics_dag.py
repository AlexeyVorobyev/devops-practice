import logging

from airflow.decorators import dag, task
from pendulum import datetime

from compute_metrics_logic import (
    build_numbers,
    build_report,
    calculate_average,
    calculate_maximum,
    calculate_sum,
)


@dag(
    dag_id="compute_metrics",
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["lab1"],
)
def compute_metrics():
    @task
    def prepare_numbers():
        return build_numbers()

    @task
    def calculate_sum_task(numbers):
        return calculate_sum(numbers)

    @task
    def calculate_average_task(numbers):
        return calculate_average(numbers)

    @task
    def calculate_maximum_task(numbers):
        return calculate_maximum(numbers)

    @task
    def build_report_task(numbers, total, average, maximum):
        report = build_report(numbers, total, average, maximum)
        logging.info("Metrics report: %s", report)
        return report

    numbers = prepare_numbers()
    total = calculate_sum_task(numbers)
    average = calculate_average_task(numbers)
    maximum = calculate_maximum_task(numbers)
    build_report_task(numbers, total, average, maximum)


compute_metrics()
