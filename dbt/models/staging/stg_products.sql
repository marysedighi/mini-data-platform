select
    product_id,
    name,
    category,
    price,
    rating_score,
    rating_count,
    loaded_at
from {{ source('mini_data_platform_raw_data', 'products') }}