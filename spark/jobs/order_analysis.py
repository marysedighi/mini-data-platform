from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = (
    SparkSession.builder
    .appName("Order Analysis").master("local[*]").getOrCreate()
)

orders = (
    spark.read
    .option("multiline", "true").json("data/cleaned_orders.json")
)

products = (
    spark.read
    .option("multiline", "true").json("data/cleaned_products.json")
)

users = (
    spark.read
    .option("multiline", "true").json("data/cleaned_users.json")
)   

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
        col("o.quantity") * col("p.price").alias("total_price"),
    )
)
enriched_orders.show(truncate=False)

spark.stop()
