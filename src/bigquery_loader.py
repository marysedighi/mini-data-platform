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

def load_json_to_bigquery(
    file_name: str,
    table_name: str,
    key_columns: list[str],
):
    client = get_bigquery_client()

    file_path = DATA_DIR / file_name

    with open(file_path, "r", encoding="utf-8") as file:
        rows = json.load(file)

    loaded_at = datetime.now(timezone.utc).replace(
        microsecond=0).isoformat()

    for row in rows:
        row["loaded_at"] = loaded_at

    target_table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
    staging_table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}_staging"

    target_table = client.get_table(target_table_id)

    # batch only → staging
    job_config = bigquery.LoadJobConfig(
        schema=target_table.schema,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    load_job = client.load_table_from_json(
        rows,
        staging_table_id,
        job_config=job_config,
        location="europe-west4",
    )

    load_job.result()

    columns = [field.name for field in target_table.schema]

    merge_condition = " AND ".join(
        f"T.{key} = S.{key}"
        for key in key_columns
    )

    # not change loaded_at when the row already exists
    update_columns = [
        column
        for column in columns
        if column not in key_columns
        and column != "loaded_at"
    ]

    update_clause = ", ".join(
        f"T.{column} = S.{column}"
        for column in update_columns
    )

    insert_columns = ", ".join(columns)

    insert_values = ", ".join(
        f"S.{column}"
        for column in columns
    )

    merge_query = f"""
        MERGE `{target_table_id}` AS T
        USING `{staging_table_id}` AS S
        ON {merge_condition}

        WHEN MATCHED THEN
            UPDATE SET {update_clause}

        WHEN NOT MATCHED THEN
            INSERT ({insert_columns})
            VALUES ({insert_values})
    """

    client.query(
        merge_query,
        location="europe-west4",
    ).result()

    client.delete_table(
        staging_table_id,
        not_found_ok=True,
    )

    print(f"Merged {len(rows)} rows into {target_table_id}")

# orchestration function
def load_all_tables():
    # Load all cleaned data into BQ by calling the load_json_to_bigquery function for each table
    load_json_to_bigquery("cleaned_products.json", 
                          "products", 
                          ["product_id"]
                          )
    
    load_json_to_bigquery("cleaned_users.json",
                          "users",
                          ["user_id"]
                          )

    load_json_to_bigquery("cleaned_orders.json",
                           "orders", 
                           ["order_id", "product_id"]
                           )

if __name__ == "__main__":
    load_all_tables()