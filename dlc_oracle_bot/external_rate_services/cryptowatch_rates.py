from datetime import datetime, timezone
import os

import cryptowatch as cw
from dotenv import load_dotenv

load_dotenv()

cw.api_key = os.environ['CRYPTOWATCH_PUBLIC_KEY']


class CryptowatchRates(object):

    def __init__(self):
        self.cache = {}

    def get_daily_close(self, timestamp: datetime, exchange: str, pair: str):
        datetime_requested_truncated = timestamp.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        ticker = "{}:{}".format(exchange, pair).upper()
        if not self.cache.get(ticker):
            self.cache[ticker] = cw.markets.get(ticker, ohlc=True, periods=['1d'])
        for candle in self.cache[ticker].of_1d:
            close_timestamp, open_px, high, low, close, volume, volume_quote = candle
            close_ts = datetime.fromtimestamp(close_timestamp, tz=timezone.utc)
            if datetime_requested_truncated == close_ts:
                return close
        return None
