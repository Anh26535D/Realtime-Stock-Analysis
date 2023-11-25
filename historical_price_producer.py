from datetime import timedelta
import time

import pandas as pd
from tqdm import tqdm
from kafka import Producer

from crawler.CafeF import HistoricalPriceCafef
from utils.logger.Logger import Logger

MAX_DAY = 100

date_logger = Logger(r'logs\date_logs\datemapping.log')
crawler = HistoricalPriceCafef()

symbols = pd.read_csv('data/list_companies.csv')['Mã CK▲']
symbols = ['AAA']

producer_config = {
    'bootstrap.servers': 'localhost:9092',
}
producer = Producer(producer_config)

kafka_topic = 'historical price'
for day in tqdm(range(MAX_DAY)):
    for symbol in symbols:
        data = crawler.getHistoricalPrice(
            symbol=symbol,
            start_date=date_logger.latest_system_time,
            end_date=date_logger.latest_system_time
        )

        for _, row in data.iterrows():
            message_value = row.to_dict()
            producer.produce(kafka_topic, value=message_value)

    time.sleep(5)
    date_logger.latest_system_time = date_logger.latest_system_time + timedelta(days=1)
    date_logger.log_time_system()
producer.flush()
