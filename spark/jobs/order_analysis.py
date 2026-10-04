from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum
from spark.schemas.schemas import (
    orders_schema,
    products_schema,
    users_schema,
)

def main():
    
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

    products = (
        spark.read
        .schema(products_schema)
        .option("multiline", "true")
        .json("data/cleaned_products.json")
    )

    users = (
        spark.read
        .schema(users_schema)
        .option("multiline", "true")
        .json("data/cleaned_users.json")
    )      

    # Validate the data
    validate_orders(orders)
    validate_products(products)
    validate_users(users)
    validate_references(orders, products, users)

    # Enrich orders with product and user information
    enriched_orders = enrich_orders(orders, products, users)

    # Calculate revenue by category
    revenue_by_category = calculate_revenue_by_category(enriched_orders)

    # Calculate top 10 users by total spent
    top_users = calculate_top_users(enriched_orders)

    # Calculate top 10 products by total revenue
    top_products = calculate_top_products(enriched_orders)

    # Save the results to Parquet files
    revenue_by_category.write.mode("overwrite").parquet(
        "data/spark/revenue_by_category")

    top_users.write.mode("overwrite").parquet(
        "data/spark/top_users")

    top_products.write.mode("overwrite").parquet(
        "data/spark/top_products")

    print("Spark order analysis completed successfully.")

    spark.stop()

# check for invalid orders
def validate_orders(orders):
    invalid_orders = orders.filter(
        col("order_id").isNull()
        | col("user_id").isNull()
        | col("product_id").isNull()
        | col("quantity").isNull()
        | (col("quantity") <= 0)
    )
    if invalid_orders.take(1):
        raise ValueError("Invalid orders found")

# check for invalid products
def validate_products(products):
    invalid_products = products.filter(
        col("product_id").isNull()
        | col("name").isNull()
        | col("category").isNull()
        | col("price").isNull()
        | (col("price") < 0)
    )
    if invalid_products.take(1):
        raise ValueError("Invalid products found")

# check for invalid users (e.g., missing user_id)
def validate_users(users):
    if users.filter(col("user_id").isNull()).take(1):
        raise ValueError("Invalid users found")

# check orders for missing products & users
def validate_references(orders, products, users):
    if orders.join(products, on="product_id", how="left_anti").take(1):
        raise ValueError("Orders reference unknown products")

    if orders.join(users, on="user_id", how="left_anti").take(1):
        raise ValueError("Orders reference unknown users")

# Enrich orders with join product and user information
def enrich_orders(orders, products, users):
    return (
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
def calculate_revenue_by_category(enriched_orders):
    return (
        enriched_orders
        .groupBy("category")
        .agg(spark_sum("total_price").alias("total_revenue"))
        .orderBy(col("total_revenue").desc())
    )

# get top 10 users
def calculate_top_users(enriched_orders):
    return (
        enriched_orders
        .groupBy("user_id", "user_name")
        .agg(spark_sum("total_price").alias("total_spent"))
        .orderBy(col("total_spent").desc())
        .limit(10)
    )


# get top 10 products
def calculate_top_products(enriched_orders):
    return (
        enriched_orders
        .groupBy("product_id", "product_name")
        .agg(spark_sum("total_price").alias("total_revenue"))
        .orderBy(col("total_revenue").desc())
        .limit(10)
    )


if __name__ == "__main__":
    main()
