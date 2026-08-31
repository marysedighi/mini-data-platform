from google.cloud import bigquery

PROJECT_ID = "mini-data-platform-507211"
DATASET_ID = "mini_data_platform"

def get_bigquery_client():
    """
    Returns a BigQuery client for the specified project.
    """
    return bigquery.Client(project=PROJECT_ID)