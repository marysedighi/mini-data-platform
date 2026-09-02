# 🏗️ Mini Data Platform

A hands-on data engineering project that ingests product, user, and order data, cleans and validates it, stores it in SQLite, exposes analytics through a FastAPI service, caches selected API responses in Redis, and orchestrates the ETL flow with Apache Airflow.

The project is also set up for containerized local development with Docker Compose and CI validation with GitHub Actions.

## Architecture

```text
Fake Store API / local JSON fallback
        |
        v
Python ETL pipelines
        |
        v
Cleaned JSON files in data/
        |
        v
SQLite database
        |
        +--> SQL analytics queries
        |
        +--> FastAPI REST API
                |
                v
              Redis cache

Optional cloud path:
Cleaned JSON files -> BigQuery schema setup -> BigQuery table loads

Orchestration:
Apache Airflow DAG -> ETL pipelines -> data quality checks
```

## ⚙️ Infrastructure

The local infrastructure is defined in `compose.yaml`.

| Service | Purpose | Port |
| --- | --- | --- |
| `api` | FastAPI app served by Uvicorn | `8000` |
| `redis` | Cache for API analytics responses | internal `6379` |
| `airflow-db` | PostgreSQL metadata database for Airflow | internal |
| `airflow-init` | Runs Airflow database migrations | none |
| `airflow` | Airflow standalone webserver/scheduler | `8080` |

The API container mounts:

- `./src:/app/src`
- `./data:/app/data`

The Airflow container mounts:

- `./airflow/dags:/opt/airflow/dags`
- `./src:/opt/airflow/src`
- `./data:/opt/airflow/data`

## 📁 Project Structure

```text
mini-data-platform/
├── airflow/
│   └── dags/
│       ├── airflow_test_dag.py
│       └── etl_pipeline_dag.py
├── bigquery/
│   └── schemas/
│       ├── orders.sql
│       ├── products.sql
│       └── users.sql
├── data/
│   ├── cleaned_orders.json
│   ├── cleaned_products.json
│   ├── cleaned_users.json
│   ├── mini_data_platform.db
│   ├── products.json
│   └── users.json
├── src/
│   ├── analytics.py
│   ├── api.py
│   ├── bigquery_client.py
│   ├── bigquery_loader.py
│   ├── bigquery_setup.py
│   ├── cache.py
│   ├── data_quality.py
│   ├── database.py
│   ├── etl.py
│   └── main.py
├── tests/
│   ├── test_analytics.py
│   ├── test_api.py
│   ├── test_data_quality.py
│   ├── test_database.py
│   └── test_etl.py
├── .github/workflows/python-ci.yml
├── Dockerfile
├── compose.yaml
├── requirements.txt
└── README.md
```

## ✨ Features

### Batch ETL

- Fetches products, users, and orders from external APIs.
- Falls back to local JSON files when needed.
- Cleans, normalizes, and validates records.
- Saves cleaned datasets to `data/`.
- Loads cleaned data into SQLite.
- Includes logging, retries, and error handling.

### SQLite Data Store

The local database is stored at:

```text
data/mini_data_platform.db
```

Current tables:

- `products`
- `users`
- `orders`

The schema supports product, user, and order analytics with foreign key relationships between orders, users, and products.

### ✅ Data Quality Checks

Implemented checks include:

- Null product fields
- Null user fields
- Duplicate products
- Duplicate users
- Orders with invalid user or product references
- Row counts for products, users, and orders

### 📊 SQL Analytics

Implemented analytics include:

- Product count
- Average product price
- Products by category
- Products above a selected price
- Top expensive products
- Price segmentation
- Category price summary with CTEs
- Ranked products by price with window functions
- Highest-rated products
- Revenue per category
- Orders with user and product details
- Top products by purchased quantity
- Top users by order count
- Product lookup by ID

### 🚀 FastAPI Service

The API is defined in `src/api.py`.

Available endpoints:

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/health` | API status and Redis connection status |
| `GET` | `/analytics/summary` | Product count and revenue by category, cached for 60 seconds |
| `GET` | `/analytics/top-users` | Top users by order count |
| `GET` | `/top_rated_products` | Highest-rated products |
| `GET` | `/products/{product_id}` | Product details by ID |

API documentation is available at:

```text
http://localhost:8000/docs
```

### Redis Cache

Redis is used by the API service for cached analytics responses. The Docker Compose setup passes these environment variables to the API container:

```text
REDIS_HOST=redis
REDIS_PORT=6379
```

### Apache Airflow

Airflow orchestration is implemented in:

```text
airflow/dags/etl_pipeline_dag.py
```

The `etl_pipeline` DAG runs:

1. Products pipeline
2. Users pipeline
3. Orders pipeline
4. Data quality checks

There is also a small test DAG at:

```text
airflow/dags/airflow_test_dag.py
```

Airflow UI:

```text
http://localhost:8080
```

### ☁️ BigQuery

BigQuery support is included through:

- `src/bigquery_client.py`
- `src/bigquery_setup.py`
- `src/bigquery_loader.py`
- `bigquery/schemas/*.sql`

Current BigQuery configuration:

```text
PROJECT_ID=mini-data-platform-507211
DATASET_ID=mini_data_platform
LOCATION=europe-west4
```

The setup script runs the SQL schema files. The loader script loads cleaned JSON data into the existing BigQuery tables with `WRITE_TRUNCATE`.

### CI

GitHub Actions is configured in:

```text
.github/workflows/python-ci.yml
```

The CI workflow runs on pushes and pull requests to `main`. It:

- Checks out the repository
- Sets up Python 3.12
- Installs dependencies
- Runs `pytest`
- Runs `python -m src.main`

## ▶️ Run Locally

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

For fish shell:

```fish
source venv/bin/activate.fish
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the ETL pipeline and analytics:

```bash
python -m src.main
```

Run tests:

```bash
python -m pytest
```

Start the API locally without Docker:

```bash
uvicorn src.api:app --reload
```

## 🐳 Run With Docker Compose

Build and start all services:

```bash
docker compose up -d --build
```

Run the ETL pipeline inside the API container:

```bash
docker compose exec api python -m src.main
```

Open the API docs:

```text
http://localhost:8000/docs
```

Open Airflow:

```text
http://localhost:8080
```

Check running services:

```bash
docker compose ps
```

Stop services:

```bash
docker compose down
```

Stop services and remove the Airflow metadata database volume:

```bash
docker compose down -v
```

## BigQuery Workflow

Authenticate with Google Cloud before running BigQuery scripts:

```bash
gcloud auth application-default login
```

Create or update BigQuery tables from SQL schema files:

```bash
python -m src.bigquery_setup
```

Load cleaned JSON data into BigQuery:

```bash
python -m src.bigquery_loader
```

## Tech Stack

Current:

- Python 3.12
- FastAPI
- Uvicorn
- SQLite
- Redis
- Apache Airflow
- Docker
- Docker Compose
- Google BigQuery client
- Pytest
- GitHub Actions

Planned or future enhancements:

- dbt analytics engineering
- Kafka streaming
- Spark batch and streaming jobs
- Apache Beam / Google Dataflow
- Terraform infrastructure as code
- Databricks

## 🎓 Learning Focus

This project is designed to practice:

- Python for data engineering
- Batch ETL pipelines
- REST API ingestion
- Data cleaning and normalization
- Data validation and data quality checks
- SQLite database design
- SQL analytics
- Joins, CTEs, and window functions
- FastAPI API development
- Redis caching
- Dockerized development
- Airflow orchestration
- BigQuery table setup and loading
- Unit testing with Pytest
- CI with GitHub Actions
