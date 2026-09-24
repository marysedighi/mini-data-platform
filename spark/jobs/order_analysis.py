from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum
from spark.schemas.schemas import (
    orders_schema,
    products_schema,
    users_schema,
)

# Initialize Spark session
spark = (
    SparkSession.builder
    .appName("Order Analysis")
    .master("local[*]")
    .getOrCreate()
)

# Read the cleaned data files into DataFrames
orders = (
    spark.read
    .schema(orders_schema)
    .option("multiline", "true")
    .json("data/cleaned_orders.json")
)

# Validate the orders DataFrame for any invalid records
invalid_orders = orders.filter(
    col("order_id").isNull()
    | col("user_id").isNull()
    | col("product_id").isNull()
    | col("quantity").isNull()
    | (col("quantity") <= 0)
)

if invalid_orders.take(1):
    raise ValueError("Invalid orders found")

products = (
    spark.read
    .schema(products_schema)
    .option("multiline", "true")
    .json("data/cleaned_products.json")
)

# check for invalid products (e.g., missing product_id or price)
invalid_products = products.filter(
    col("product_id").isNull()
    | col("name").isNull()
    | col("category").isNull()
    | col("price").isNull()
    | (col("price") < 0)
)   

if invalid_products.take(1):
    raise ValueError("Invalid products found")

users = (
    spark.read
    .schema(users_schema)
    .option("multiline", "true")
    .json("data/cleaned_users.json")
)      

# check for invalid users (e.g., missing user_id)
invalid_users = users.filter(
    col("user_id").isNull()
)

if invalid_users.take(1):
    raise ValueError("Invalid users found")

# check orders referencing unknown products
missing_products = (
    orders.join(products, on="product_id", how="left_anti")
)
if missing_products.take(1):
    raise ValueError("Orders with missing product_id found")

# check ordrers referencing unknown users
missing_users = (
    orders.join(users, on="user_id", how="left_anti")
)
if missing_users.take(1):
    raise ValueError("Orders with missing user_id found")

# Enrich orders with join product and user information
enriched_orders = (
    orders.alias("o")
    .join(products.alias("p"), col("o.product_id") == col("p.product_id"), "inner")
    .join(users.alias("u"), col("o.user_id") == col("u.user_id"), "inner")
    .select(
        col("o.order_id"),
        col("o.user_id"),
        col("o.product_id"),
        col("o.order_date"),
        col("o.quantity"),
        col("p.name").alias("product_name"),
        col("p.category"),
        col("p.price"),
        col("u.name").alias("user_name"),
        (col("o.quantity") * col("p.price")).alias("total_price"),
    )
)

# get revenue by category
revenue_by_category = (
    enriched_orders
    .groupBy("category")
    .agg(
        spark_sum("total_price").alias("total_revenue")
    )
    .orderBy(col("total_revenue").desc())
)

print("Revenue by category:")
revenue_by_category.show(truncate=False)

# get top 10 users
top_users = (
    enriched_orders
    .groupBy("user_id", "user_name")
    .agg(
        spark_sum("total_price").alias("total_spent")
    )
    .orderBy(col("total_spent").desc())
    .limit(10)
)

print("Top users:")
top_users.show(truncate=False)

# get top 10 products
top_products = (
    enriched_orders
    .groupBy("product_id", "product_name")
    .agg(
        spark_sum("total_price").alias("total_revenue")
    )
    .orderBy(col("total_revenue").desc())
    .limit(10)
)

print("Top products:")
top_products.show(truncate=False)

# Save the results to Parquet files
revenue_by_category.write.mode("overwrite").parquet(
    "data/spark/revenue_by_category")

top_users.write.mode("overwrite").parquet(
    "data/spark/top_users")

top_products.write.mode("overwrite").parquet(
    "data/spark/top_products")


spark.stop()
