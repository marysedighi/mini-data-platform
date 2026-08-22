from datetime import datetime, timedelta

from airflow.sdk import DAG, task

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

    @task
    def process_users():
        users_pipeline()

    @task
    def process_orders():
        orders_pipeline()

    @task
    def run_data_quality():
        print("Null products:", check_null_products())
        print("Duplicate products:", check_duplicate_products())
        print("Null users:", check_null_users())
        print("Duplicate users:", check_duplicate_users())
        print(
            "Invalid order references:",
            check_orders_with_invalid_references(),
        )
        print("Row counts:", check_row_counts())

    products = process_products()
    users = process_users()
    orders = process_orders()
    quality = run_data_quality()

    [products, users] >> orders >> quality