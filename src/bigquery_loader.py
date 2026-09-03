import json
from pathlib import Path

from google.cloud import bigquery
from datetime import datetime, timezone

from src.bigquery_client import (
    get_bigquery_client,
    PROJECT_ID,
    DATASET_ID,
)

# Path to the local cleaned JSON files
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_json_to_bigquery(file_name: str, table_name: str):
    # Connect to BigQuery
    client = get_bigquery_client()

    # find the json file
    file_path = DATA_DIR / file_name

    # Read cleaned data from json
    with open(file_path, "r", encoding="utf-8") as file:
        rows = json.load(file)

        loaded_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

        for row in rows:
            row["loaded_at"] = loaded_at

    #Full BQ table name: project_id.dataset_id.table_name
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

    # Get existing BQ table and schema
    table = client.get_table(table_id)

    # use the existing schema and replace old table data -  WRITE_TRUNCATE write data with repalce them and avoid duplicates
    job_config = bigquery.LoadJobConfig(
        schema=table.schema,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    # start the BQ load job
    job = client.load_table_from_json(
        rows,
        table_id,
        job_config=job_config,
        location="europe-west4",
    )

    # write until BQ finishes loading the data
    job.result()

    print(f"Loaded {len(rows)} rows into {table_id}")


def load_all_tables():
    # Load all cleaned data into BQ by calling the load_json_to_bigquery function for each table
    load_json_to_bigquery("cleaned_products.json", "products")
    load_json_to_bigquery("cleaned_users.json", "users")
    load_json_to_bigquery("cleaned_orders.json", "orders")


if __name__ == "__main__":
    load_all_tables()