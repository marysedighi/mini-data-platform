SELECT
    product_id,
    name as product_name,
    category,
    price,
    rating_score,
    rating_count
from {{ ref('stg_products') }}