from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count

spark = (
    SparkSession.builder
    .appName("Product Analysis").master("local[*]").getOrCreate()
)

products = (
    spark.read
    .option("multiline", "true").json("data/cleaned_products.json")
)

print("products schema:")
products.printSchema()

category_summary =  (
    products.groupBy("category").agg(
        count("product_id").alias("product_count"),
        avg("price").alias("average_price") 
        )
    .orderBy("category")
)

category_summary.show(truncate=False)

category_summary.write.mode("overwrite").parquet("data/spark/category_summary.parquet")

spark.stop()
