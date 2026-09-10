select
    user_id,
    name,
    email,
    city,
    street,
    zipcode,
    phone,
    loaded_at
from {{ source('mini_data_platform_raw_data', 'users') }}