# Mini Data Platform

A simple Data Engineering project inspired by real-world recommendation and ETL systems.

## 🚀 Project Goals

This project demonstrates:

- ETL/ELT concepts
- API data ingestion
- Data cleaning and transformation
- Python testing
- Docker containerization
- GitHub Actions CI
- integration with:
  - Kafka
  - Apache Beam / Dataflow
  - Spark
  - BigQuery / Data Warehouse
  - Redis caching
  - Terraform

---

# 🏗️ Project Structure

```text
mini-data-platform/
├── src/
│   ├── main.py
│   └── etl.py
├── tests/
│   └── test_etl.py
├── data/
│   ├── products.json
│   └── cleaned_products.json
├── .github/workflows/
│   └── python-ci.yml
├── Dockerfile
├── .dockerignore
├── requirements.txt
└── README.md
```

---

# ⚙️ Features Implemented

## ✅ ETL Pipeline

Current ETL flow:

1. Extract product data from external API
2. Transform and clean product data
3. Load cleaned data into JSON storage

---

## ✅ API Ingestion

Uses:

- `requests`
- Fake Store API

Example endpoint:

```text
https://fakestoreapi.com/products
```

---

## ✅ Data Cleaning

Transformation examples:

- remove invalid products
- normalize categories
- trim extra spaces
- enforce numeric price type
- rename fields

---

## ✅ Testing

Uses:

- `pytest`

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

CI pipeline automatically:

- installs dependencies
- runs tests
- runs ETL pipeline

---

# 🛠️ Tech Stack

- Python
- Pytest
- Docker
- GitHub Actions
- REST APIs

Planned:
- Kafka
- Apache Beam
- Dataflow
- Spark
- BigQuery
- Redis
- Terraform

---

# ▶️ Run Locally

Create virtual environment:

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate.fish
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run project:

```bash
python src/main.py
```

---

# 📚 Learning Focus

This repository is focused on learning:

- Data Engineering fundamentals
- ETL pipelines
- API integration
- Testing
- CI/CD
- Containerization
- Data processing
- SQL and analytics concepts