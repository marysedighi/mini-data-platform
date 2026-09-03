CREATE TABLE IF NOT EXISTS
  `mini-data-platform-507211.mini_data_platform.users`
(
  user_id INT64 NOT NULL,
  name STRING NOT NULL,
  email STRING NOT NULL,
  city STRING,
  street STRING,
  zipcode STRING,
  phone STRING,
  loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);