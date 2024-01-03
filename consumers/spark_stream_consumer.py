import sys
sys.path.append("/app")
import os

import findspark
findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.types import StructType, StructField, StringType
from dotenv import load_dotenv
load_dotenv()

from InfluxDBWriter import InfluxDBWriter

KAFKA_TOPIC_NAME = "historical_price"
KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"

scala_version = '2.12'
spark_version = '3.3.3'
packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.4.0'
]

token = os.environ.get("INFLUX_TOKEN")
host = "http://influxdb:8086"
bucket = os.environ.get("INFLUX_BUCKET")
measurement = "stock_price"
org = os.environ.get("INFLUX_ORG")

if __name__ == "__main__":
    spark = (
        SparkSession.builder.appName("StockPriceConsumer")
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
    influxdb_writer = InfluxDBWriter(
        url=host,
        token=token,
        bucket=bucket,
        measurement=measurement,
        org=org,
    )

    def process_batch(batch_df, batch_id):
        print(f"Processing batch {batch_id}")
        realtimeStockPrices = batch_df.select("stock_price.*")
        for realtimeStockPrice in realtimeStockPrices.collect():
            timestamp = realtimeStockPrice["date"]
            tags = {"stock_symbol": realtimeStockPrice["stock_symbol"]}
            fields = {
                "open": realtimeStockPrice['open'],
                "close": realtimeStockPrice['close'],
                "high": realtimeStockPrice['high'],
                "low": realtimeStockPrice['low'],
                "volume": realtimeStockPrice['volume'],
                "adjusted_price": realtimeStockPrice['adjusted_price'],
                "change": realtimeStockPrice['change'],
                "trading_value": realtimeStockPrice['trading_value'],
                "negotiated_volume": realtimeStockPrice['negotiated_volume'],
                "negotiated_value": realtimeStockPrice['negotiated_value']
            }
            influxdb_writer.process(timestamp, tags, fields)
            print(f"Writing to InfluxDB: {timestamp} | {tags} | {fields}")

    query = stockDataframe \
        .writeStream \
        .foreachBatch(process_batch) \
        .outputMode("append") \
        .start()

    query.awaitTermination()