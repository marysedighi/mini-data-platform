from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    LongType,
    DoubleType,
)

orders_schema = StructType([
    StructField("order_date", StringType(), True),
    StructField("order_id", LongType(), False),
    StructField("product_id", LongType(), False),
    StructField("quantity", LongType(), False),
    StructField("user_id", LongType(), False),
])

products_schema = StructType([
    StructField("category", StringType(), True),
    StructField("name", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("product_id", LongType(), False),
    StructField("rating_count", LongType(), True),
    StructField("rating_score", DoubleType(), True),
])

users_schema = StructType([
    StructField("city", StringType(), True),
    StructField("email", StringType(), True),
    StructField("name", StringType(), True),
    StructField("phone", StringType(), True),
    StructField("street", StringType(), True),
    StructField("user_id", LongType(), False),
    StructField("zipcode", StringType(), True),
])