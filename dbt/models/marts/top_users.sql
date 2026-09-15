select
    u.user_id,
    u.name,
    u.email,
    sum(o.quantity * p.price) as total_spent,
    sum(o.quantity) as total_items
from {{ ref('stg_orders') }} o
join {{ ref('stg_users') }} u
    on o.user_id = u.user_id
join {{ ref('stg_products') }} p
    on o.product_id = p.product_id
group by
    u.user_id,
    u.name,
    u.email
order by total_spent desc