CREATE TABLE IF NOT EXISTS
  `mini-data-platform-507211.mini_data_platform.orders`
(
  order_id INT64 NOT NULL,
  user_id INT64 NOT NULL,
  product_id INT64 NOT NULL,
  quantity INT64 NOT NULL,
  order_date TIMESTAMP,
  loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);