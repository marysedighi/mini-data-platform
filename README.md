# Mini Data Platform

A simple Data Engineering project inspired by real-world recommendation and ETL systems.

## 🚀 Project Goals

This project demonstrates:


- Batch ETL pipelines
- API data ingestion (Products, Users, Orders)
- Data cleaning, normalization, and validation
- SQLite database design
- SQL analytics (SELECT, GROUP BY, JOINs, CTEs, Window Functions)
- Data quality checks
- Python unit testing with pytest
- Logging and error handling
- GitHub Actions CI
- Docker containerization

### 🔜 Planned Enhancements

- FastAPI REST API
- Redis caching
- Apache Airflow orchestration
- dbt analytics engineering
- Apache Kafka streaming
- Apache Spark (Batch & Streaming)
- Google BigQuery
- Apache Beam / Google Dataflow
- Terraform Infrastructure as Code

---

# 🏗️ Project Structure

```text
mini-data-platform/
├── src/
│   ├── __init__.py
│   ├── main.py                # Runs ETL pipelines and analytics
│   ├── etl.py                 # Extract, clean and validate data
│   ├── database.py            # SQLite tables and insert operations
│   └── analytics.py           # SQL analytics queries
│
├── tests/
│   ├── test_etl.py
│   ├── test_database.py
│   └── test_analytics.py
│
├── data/
│   ├── products.json
│   ├── users.json
│   ├── orders.json
│   ├── cleaned_products.json
│   ├── cleaned_users.json
│   ├── cleaned_orders.json
│   └── mini_data_platform.db
│
├── .github/
│   └── workflows/
│       └── python-ci.yml
│
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# ⚙️ Features Implemented

## ✅ Batch ETL Pipeline

* Extract products, users, and orders from Fake Store APIs
* Fallback to local JSON files
* Clean, normalize, and validate data
* Save cleaned data to JSON
* Load cleaned data into SQLite
* ETL pipeline orchestration
* Error handling and retry logic
* Logging

---

## ✅ Database Layer

Uses **SQLite** for persistent local storage.

Implemented:

* Products table
* Users table
* Orders table
* Composite primary key
* Foreign key relationships
* Insert pipelines
* Database unit tests

### Database Schema

**products**

* product_id
* name
* category
* price
* rating_score
* rating_count

**users**

* user_id
* name
* email
* city
* street
* zipcode
* phone

**orders**

* order_id
* user_id
* product_id
* quantity
* order_date

---

## ✅ SQL Analytics

Implemented analytical queries:

* Product count
* Average product price
* Products per category
* Products above a given price
* Top expensive products
* Price segmentation
* Category price summary (CTE)
* Ranked products by price (Window Function)
* Highest-rated products
* Revenue per category
* Orders with user and product details (JOIN)
* Top products by quantity purchased
* Top users by order count

---

## ✅ API Ingestion

Technologies:

* Python `requests`
* Fake Store API

Endpoints:

* `/products`
* `/users`
* `/carts`

---

## ✅ Data Cleaning

Implemented transformations:

* Remove invalid records
* Normalize categories
* Trim extra spaces
* Convert price to numeric type
* Rename API fields
* Flatten nested order/cart data

---

## ✅ Testing

Uses **pytest**.

Covered:

* ETL unit tests
* Database unit tests
* Analytics unit tests

Run tests:

```bash
python -m pytest
```

---

## ✅ Docker

Build image:

```bash
docker build -t mini-data-platform .
```

Run container:

```bash
docker run mini-data-platform
```

---

## ✅ GitHub Actions

Continuous Integration automatically:

* Installs dependencies
* Runs unit tests
* Executes the ETL pipeline

# 🛠️ Tech Stack

## Current

* Python
* SQLite
* SQL
* Pytest
* Docker
* GitHub Actions
* REST APIs
* Logging

## Planned

* FastAPI
* Redis
* Apache Airflow
* dbt
* Apache Kafka
* Apache Spark (Batch & Streaming)
* Google BigQuery
* Apache Beam / Google Dataflow
* Terraform

---

# ▶️ Run Locally

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

**macOS / Linux**

```bash
source venv/bin/activate
```

**Fish shell**

```bash
source venv/bin/activate.fish
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python -m src.main
```

Run unit tests:

```bash
python -m pytest
```

---

# 📚 Learning Focus

This project is designed to practice real-world Data Engineering concepts, including:

* Python for Data Engineering
* Batch ETL pipelines
* REST API integration
* Data cleaning, normalization and validation
* SQLite database design
* Data modeling fundamentals
* SQL fundamentals
* SQL aggregations
* GROUP BY, WHERE and CASE WHEN
* JOINs
* CTEs
* Window Functions
* Unit testing with Pytest
* Logging and error handling
* GitHub Actions (CI/CD)
* Docker containerization
* Data quality concepts
* BigQuery fundamentals
* Apache Airflow
* dbt
* Apache Kafka
* Apache Spark
* Apache Beam / Google Dataflow
* Terraform