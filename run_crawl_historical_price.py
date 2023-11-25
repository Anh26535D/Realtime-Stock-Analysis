from datetime import timedelta
import time
from tqdm import tqdm
import os

import pandas as pd

from crawler.CafeF import HistoricalPriceCafef
from utils.logger.Logger import Logger

date_logger = Logger(r'logs\date_logs\datemapping.log')
crawler = HistoricalPriceCafef()


symbols = pd.read_csv('data/list_companies.csv')['Mã CK▲']
symbols = ['AAA']
                        
for symbol in symbols:
    for _ in tqdm(range(10)):
        data = crawler.getHistoricalPrice(
            symbol=symbol, 
            start_date=date_logger.latest_system_time, 
            end_date=date_logger.latest_system_time
        )
        if os.path.isfile('temp.csv') and os.path.getsize('temp.csv') > 0:
            data.to_csv('temp.csv', mode='a', index=False, header=False)
        else:
            data.to_csv('temp.csv', index=False)
        date_logger.latest_system_time = date_logger.latest_system_time + timedelta(days=1)
        time.sleep(5)

date_logger.log_time_system()