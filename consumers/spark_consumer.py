import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType


# Set up Spark session
spark = SparkSession.builder.appName("KafkaConsumerApp").getOrCreate()

# Define schema for the data
schema = StructType([
    StructField("date", StringType()),
    StructField("open", DoubleType()),
    StructField("close", DoubleType()),
    StructField("high", DoubleType()),
    StructField("low", DoubleType()),
    StructField("volume", IntegerType()),
    StructField("adjusted_price", DoubleType()),
    StructField("change", StringType()),
    StructField("trading_value", DoubleType()),
    StructField("negotiated_volume", IntegerType()),
    StructField("negotiated_value", DoubleType())
])

# Set up Kafka consumer
kafka_topic = 'historical_price'
kafka_bootstrap_servers = 'localhost:9093'

df = (
    spark
    .readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers)
    .option("subscribe", kafka_topic)
    .load()
    .selectExpr("CAST(value AS STRING)")
    .select(from_json(col("value"), schema).alias("data"))
    .select("data.*")
)

# Define the sink
postgres_config = {
    'url': f"jdbc:postgresql://{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}",
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'dbtable': 'historical_prices',
    'driver': 'org.postgresql.Driver'
}

query = (
    df
    .writeStream
    .outputMode("append")
    .foreachBatch(lambda batch, batch_id: batch.write.jdbc(**postgres_config))
    .start()
)

# Wait for termination
query.awaitTermination()