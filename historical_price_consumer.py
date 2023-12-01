from kafka import KafkaConsumer
import json
import psycopg2
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

bootstrap_servers = 'localhost:9093'
kafka_topic = 'historical_price'
consumer = KafkaConsumer(
    kafka_topic,
    bootstrap_servers=bootstrap_servers,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    # auto_offset_reset='earliest' # read from the begin of the partition
)

postgres_config = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT')
}

conn = psycopg2.connect(**postgres_config)
cursor = conn.cursor()

create_table_query = '''
CREATE TABLE IF NOT EXISTS historical_prices (
    date DATE,
    open NUMERIC,
    close NUMERIC,
    high NUMERIC,
    low NUMERIC,
    volume INT,
    adjusted_price NUMERIC,
    change TEXT,
    trading_value NUMERIC,
    negotiated_volume INT,
    negotiated_value NUMERIC
);
'''
cursor.execute(create_table_query)
conn.commit()

for message in consumer:
    data = message.value
    if data['date'] is not None:
        try:
            data['date'] = datetime.strptime(data['date'], '%d/%m/%Y').strftime('%Y-%m-%d')
        except ValueError:
            data['date'] = None

        insert_query = '''
        INSERT INTO historical_prices VALUES (
            %(date)s, %(open)s, %(close)s, %(high)s, %(low)s,
            %(volume)s, %(adjusted_price)s, %(change)s, %(trading_value)s,
            %(negotiated_volume)s, %(negotiated_value)s
        );
        '''

        cursor.execute(insert_query, data)
        conn.commit()

        print(f"Inserted data into PostgreSQL: {data['date']}")

consumer.close()
cursor.close()
conn.close()
