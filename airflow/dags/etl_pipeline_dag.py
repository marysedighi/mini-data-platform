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

import logging

logger = logging.getLogger(__name__)

# Define callback functions for DAG success and failure
def log_dag_success(context):
    dag_run = context["dag_run"]

    logger.info(
        "ETL pipeline completed successfully. run_id=%s",
        dag_run.run_id,
    )


def log_dag_failure(context):
    dag_run = context["dag_run"]
    task_instance = context["task_instance"]

    logger.error(
        "ETL pipeline failed. run_id=%s failed_task=%s",
        dag_run.run_id,
        task_instance.task_id,
    )

with DAG(
    dag_id="etl_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    on_success_callback=log_dag_success,
    on_failure_callback=log_dag_failure,
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

    @task(trigger_rule=TriggerRule.ALL_SUCCESS)
    def run_data_quality():
        null_products = check_null_products()
        duplicate_products = check_duplicate_products()
        null_users = check_null_users()
        duplicate_users = check_duplicate_users()
        invalid_references = check_orders_with_invalid_references()
        row_counts = check_row_counts()

        logger.info("Null products: %s", null_products)
        logger.info("Duplicate products: %s", duplicate_products)
        logger.info("Null users: %s", null_users)
        logger.info("Duplicate users: %s", duplicate_users)
        logger.info("Invalid order references: %s", invalid_references)
        logger.info("Row counts: %s", row_counts)

        if (
            null_products > 0
            or duplicate_products
            or null_users > 0
            or duplicate_users
            or invalid_references
        ):
            raise ValueError("Data quality checks failed")

        logger.info("Data quality checks passed")

    @task
    def load_to_bigquery():
        load_all_tables()
        return "Data loaded to BigQuery"

    products = process_products()
    users = process_users()
    orders = process_orders()
    quality = run_data_quality()
    bigquery_load = load_to_bigquery()

    [products, users] >> orders >> quality >> bigquery_load