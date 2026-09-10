select
    order_id,
    user_id,
    product_id,
    quantity,
    order_date,
    loaded_at
from {{ source('mini_data_platform_raw_data', 'orders') }}