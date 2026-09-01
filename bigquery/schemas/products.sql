CREATE TABLE IF NOT EXISTS
  `mini-data-platform-507211.mini_data_platform.products`
(
  product_id INT64 NOT NULL,
  name STRING NOT NULL,
  category STRING NOT NULL,
  price FLOAT64 NOT NULL,
  rating_score FLOAT64,
  rating_count INT64
);