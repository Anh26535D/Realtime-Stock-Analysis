from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from datetime import datetime
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType

schema = StructType([
    StructField("date", DateType()),
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

scala_version = '2.12'
spark_version = '3.4.2'
packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:2.8.1'
]
spark = (
    SparkSession.builder.appName("KafkaSparkConsumer")
    .master("local")
    .config("spark.jars.packages", ",".join(packages))
    .getOrCreate()
)

# Configure Kafka parameters
kafka_params = {
    "kafka.bootstrap.servers": "localhost:9093",
    "subscribe": "historical_price",
    "startingOffsets": "earliest"
}

kafka_stream_df = spark.readStream.format("kafka").options(**kafka_params).load()
parsed_stream_df = kafka_stream_df.selectExpr("CAST(value AS STRING)").select(from_json("value", schema).alias("data")).select("data.*")

def process_row(row):
    data = row.asDict()
    if data['date'] is not None:
        data['date'] = datetime.strptime(data['date'], '%d/%m/%Y').strftime('%Y-%m-%d')

    print(f"Inserted data into PostgreSQL: {data['date']}")

query = parsed_stream_df.writeStream.foreach(process_row).start()

query.awaitTermination()
