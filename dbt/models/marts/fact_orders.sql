{{ config(
    materialized='table',
    partition_by={
        "field": "order_date",
        "data_type": "date",
        "granularity": "day"
    },
    cluster_by=["user_id", "product_id"]
) }}
select
    o.order_id,
    o.user_id,
    o.product_id,
    o.quantity,
    DATE(SAFE_CAST(o.order_date AS TIMESTAMP)) as order_date,
    p.price as product_price,
    (o.quantity * p.price) as total_order_value
from {{ ref('stg_orders') }} o
join {{ ref('stg_products') }} p
    on o.product_id = p.product_id