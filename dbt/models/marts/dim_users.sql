SELECT
    user_id,
    name,
    email,
    city,
    street,
    zipcode,
    phone,
from {{ ref('stg_users') }}