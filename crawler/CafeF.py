import json
from dateutil import relativedelta
from datetime import datetime
import requests

import pandas as pd

from crawler.common import CafefCommon

class HistoricalPriceCafef():
    '''Crawl historical price from CafeF'''

    def __init__(self):
        self.HISTORICAL_PRICE_URL = CafefCommon.HISTORICAL_PRICE_URL

    def getHistoricalPrice(self, symbol, start_date=None, end_date=None, yrs_delta=1) -> pd.DataFrame:
        '''
        Get historical price

        Parameters
        ----------
        symbol: str

        start_date: str
            Start date with format %m/%d/%Y
        
        end_date: str
            End date with format %m/%d/%Y

        yrs_delta: int
            Relative delta year between start_date and end_date.

        Returns
        -------
        data: pd.DataFrame

        '''
        symbol = symbol.upper()
        if end_date is None:
            end_date = datetime.today().strftime('%m/%d/%Y')

        if start_date is None:
            start_date = end_date - relativedelta(years=yrs_delta)
            start_date = start_date.strftime('%m/%d/%Y')

        params = {
            "Symbol": symbol,
            "StartDate": start_date,
            "EndDate": end_date,
            "PageIndex": "1",
            "PageSize": "100000"
        }

        response = requests.get(self.HISTORICAL_PRICE_URL, params=params)
        if response.status_code == 200:
            content = json.loads(response.content)
            data = content["Data"]["Data"]
            return pd.DataFrame(data)
        return pd.DataFrame(response.status_code)