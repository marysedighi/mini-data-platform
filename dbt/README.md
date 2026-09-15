# dbt - Mini Data Platform

This dbt project transforms raw data in BigQuery into clean staging models and analytics-ready mart models.

## Data flow

BigQuery raw tables
↓
dbt staging models
↓
dbt tests
↓
analytics mart models

## Sources

The dbt project uses these BigQuery source tables:

- `products`
- `users`
- `orders`

## Staging models

The staging layer provides cleaned, reusable views:

- `stg_products`
- `stg_users`
- `stg_orders`

These models are built from the BigQuery source tables.

## Mart models

The mart layer contains business-focused analytical views:

- `revenue_per_category`
- `top_products`
- `top_users`

## Testing

dbt tests are used to validate data quality, including:

- `not_null`
- `unique`
- `relationships`

Run:

```bash
dbt test
```

## Useful commands

Check the dbt configuration and BigQuery connection:

```bash
dbt debug
```
Build all dbt models:

```bash
dbt run
```
Build and test together:

```bash
dbt build
```
## BigQuery configuration

This project uses BigQuery as the analytics warehouse.

The local connection configuration is stored in:

```bash
~/.dbt/profiles.yml
```

## Model materialization

Models are currently materialized as BigQuery views.

```bash
+materialized: view
```
This means BigQuery stores the SQL definition of each model rather than physically storing a separate copy of the result data.
