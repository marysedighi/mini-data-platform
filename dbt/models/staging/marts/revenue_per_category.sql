select p.category,
    sum(o.quantity * p.price) as total_revenue
from {{ ref('stg_orders')  }} o
    join {{ ref('stg_products') }} p on o.product_id = p.product_id
group by p.category
order by total_revenue desc