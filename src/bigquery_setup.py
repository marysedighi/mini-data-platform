from pathlib import Path

from src.bigquery_client import get_bigquery_client


SCHEMA_DIR = Path(__file__).resolve().parent.parent / "bigquery" / "schemas"


def create_bigquery_tables():
    client = get_bigquery_client()

    for sql_file in SCHEMA_DIR.glob("*.sql"):
        sql = sql_file.read_text(encoding="utf-8")

        print(f"Running schema: {sql_file.name}")

        query_job = client.query(
            sql,
            location="europe-west4",
        )
        query_job.result()

        print(f"Completed: {sql_file.name}")


if __name__ == "__main__":
    create_bigquery_tables()