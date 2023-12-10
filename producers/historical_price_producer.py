import sys
sys.path.append('/app')
from datetime import timedelta
from datetime import datetime
import time
import json
import os
import datetime

import pandas as pd
from tqdm import tqdm
from confluent_kafka import Producer

from crawler.CafeF import HistoricalPriceCafef
from utils.logger.DateMappingLogger import DateMappingLogger

MAX_DAY = 100

def get_latest_data() -> pd.DataFrame:
    file_names = os.listdir('data/')
    date_format = "%Y-%m-%d"

    all_dates = []
    for fname in file_names:
        if fname.endswith('.csv'):
            cre_date = fname.split('_')[-1].split('.')[0]
            try:
                credate = datetime.datetime.strptime(cre_date, date_format)
                all_dates.append(credate)
            except:
                pass

    latest_date = max(all_dates)
    latest_fname = f'data/list_companies_{latest_date.date().strftime(date_format)}.csv'
    return pd.read_csv(latest_fname)



date_logger = DateMappingLogger(r'/app/logs/date_logs/datemapping.log')
crawler = HistoricalPriceCafef()

listing_data = get_latest_data()
symbols = listing_data['symbol']
symbols = ['AAA']

kafka_bootstrap_servers = "kafka:9092"
kafka_config = {
    "bootstrap.servers": kafka_bootstrap_servers,
}
producer = Producer(kafka_config)
kafka_topic = 'historical_price'

for day in tqdm(range(MAX_DAY)):
    for symbol in symbols:
        data = crawler.getHistoricalPrice(
            symbol=symbol,
            start_date=date_logger.latest_system_time,
            end_date=date_logger.latest_system_time
        )
        print(data)
        message_value = {
            'stock_symbol': symbol,
            'date': None,
            'open': None,
            'close': None,
            'high': None,
            'low': None,
            'volume': None,
            'adjusted_price': None,
            'change': None,
            'trading_value': None,
            'negotiated_volume': None,
            'negotiated_value': None,          
        }

        if not data.empty:
            for _, row in data.iterrows():
                message_value['date'] = row['Ngay']
                message_value['open'] = row['GiaMoCua']
                message_value['close'] = row['GiaDongCua']
                message_value['high'] = row['GiaCaoNhat']
                message_value['low'] = row['GiaThapNhat']
                message_value['volume'] = row['KhoiLuongKhopLenh']
                message_value['adjusted_price'] = row['GiaDieuChinh']
                message_value['change'] = row['ThayDoi']
                message_value['trading_value'] = row['GiaTriKhopLenh']
                message_value['negotiated_volume'] = row['KLThoaThuan']
                message_value['negotiated_value'] = row['GtThoaThuan']

                for key, value in message_value.items():
                    if pd.isnull(value):
                        message_value[key] = None

                producer.produce(kafka_topic, value=json.dumps(message_value).encode('utf-8'))
        else:
            producer.produce(kafka_topic, value=json.dumps(message_value).encode('utf-8'))
        
    time.sleep(3)
    date_logger.latest_system_time = date_logger.latest_system_time + timedelta(days=1)
    date_logger.log_time_system()

producer.flush()
producer.close()
date_logger.close()