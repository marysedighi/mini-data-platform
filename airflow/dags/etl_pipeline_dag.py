from datetime import datetime, timedelta

from airflow.sdk import DAG, task
from airflow.task.trigger_rule import TriggerRule
from src.bigquery_loader import load_all_tables

from src.main import (
    products_pipeline,
    users_pipeline,
    orders_pipeline,
)

from src.data_quality import (
    check_null_products,
    check_duplicate_products,
    check_null_users,
    check_duplicate_users,
    check_orders_with_invalid_references,
    check_row_counts,
)


with DAG(
    dag_id="etl_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=2),
    },
) as dag:

    @task
    def process_products():
        products_pipeline()
        return "Products pipeline completed"

    @task
    def process_users():
        users_pipeline()
        return "Users pipeline completed"

    @task
    def process_orders():
        orders_pipeline()
        return "Orders pipeline completed"

    @task(trigger_rule=TriggerRule.ALL_DONE)
    def report_status(status):
        print("ETL pipeline finished:", status)

    @task(trigger_rule=TriggerRule.ALL_SUCCESS)
    def run_data_quality():
        print("Null products:", check_null_products())
        print("Duplicate products:", check_duplicate_products())
        print("Null users:", check_null_users())
        print("Duplicate users:", check_duplicate_users())
        print("Invalid order references:", check_orders_with_invalid_references())
        print("Row counts:", check_row_counts())

    @task
    def load_to_bigquery():
        load_all_tables()
        return "Data loaded to BigQuery"

    products = process_products()
    users = process_users()
    orders = process_orders()
    quality = run_data_quality()
    bigquery_load = load_to_bigquery()
    status_report = report_status(orders)

    [products, users] >> orders >> quality >> bigquery_load