import os
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, max, min, count

load_dotenv()

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

spark = SparkSession.builder \
    .appName("MarketPulseSparkProcessing") \
    .config("spark.jars", "postgresql-42.7.3.jar") \
    .getOrCreate()

jdbc_url = f"jdbc:postgresql://localhost:5432/{POSTGRES_DB}"

properties = {
    "user": POSTGRES_USER,
    "password": POSTGRES_PASSWORD,
    "driver": "org.postgresql.Driver"
}

df = spark.read.jdbc(
    url=jdbc_url,
    table="stock_prices",
    properties=properties
)

aggregates_df = df.groupBy("symbol").agg(
    count("*").alias("total_records"),
    avg("close_price").alias("avg_close_price"),
    max("close_price").alias("max_close_price"),
    min("close_price").alias("min_close_price"),
    avg("volume").alias("avg_volume")
)

aggregates_df.show()

aggregates_df.write.jdbc(
    url=jdbc_url,
    table="spark_stock_aggregates",
    mode="overwrite",
    properties=properties
)

spark.stop()
