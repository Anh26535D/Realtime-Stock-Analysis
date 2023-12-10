import sys
sys.path.append("/app")

import findspark
findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.types import StructType, StructField, StringType

KAFKA_TOPIC_NAME = "historical_price"
KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"

scala_version = '2.12'
spark_version = '3.3.3'
packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.4.0'
]

if __name__ == "__main__":
    spark = (
        SparkSession.builder.appName("KafkaInfluxDBStreaming")
        .master("spark://spark-master:7077")
        .config("spark.jars.packages", ",".join(packages))
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    stockDataframe = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
        .option("subscribe", KAFKA_TOPIC_NAME) \
        .load()
    
    stockDataframe = stockDataframe.select(col("value").cast("string").alias("data"))

    inputStream =  stockDataframe.selectExpr("CAST(data as STRING)")

    stock_price_schema = StructType([
        StructField("stock_symbol", StringType(), True),
        StructField("date", StringType(), True),
        StructField("open", StringType()),
        StructField("close", StringType()),
        StructField("high", StringType()),
        StructField("low", StringType()),
        StructField("volume", IntegerType()),
        StructField("adjusted_price", StringType()),
        StructField("change", StringType()),
        StructField("trading_value", StringType()),
        StructField("negotiated_volume", IntegerType()),
        StructField("negotiated_value", StringType())
    ])

    stockDataframe = inputStream.select(from_json(col("data"), stock_price_schema).alias("stock_price"))
    expandedDf = stockDataframe.select("stock_price.*")

    def process_batch(batch_df, batch_id):
        realtimeStockPrices = batch_df.select("stock_price.*")
        for realtimeStockPrice in realtimeStockPrices.collect():
            print(realtimeStockPrice)

    query = stockDataframe \
        .writeStream \
        .foreachBatch(process_batch) \
        .outputMode("append") \
        .start()

    query.awaitTermination()