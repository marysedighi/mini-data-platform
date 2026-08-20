from airflow.sdk import DAG, task
from datetime import datetime


with DAG(
    dag_id="test_dag",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    @task
    def hello():
        print("Hello from Airflow!")

    @task
    def finish():
        print("The DAG finished successfully!")

    hello() >> finish()