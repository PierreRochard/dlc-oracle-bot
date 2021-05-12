from datetime import datetime, timezone
import os

import cryptowatch as cw
from dotenv import load_dotenv

from dlc_oracle_bot.logging_utility import log

load_dotenv()

cw.api_key = os.environ['CRYPTOWATCH_PUBLIC_KEY']


def get_close(timestamp: datetime, exchange: str, pair: str):
    ticker = "{}:{}".format(exchange, pair).upper()
    candles = cw.markets.get(ticker, ohlc=True, periods=['1d'])
    for candle in candles.of_1d:
        log.debug('candle', candle=candle)
        close_timestamp, open_px, high, low, close, volume, volume_quote = candle
        close_ts = datetime.fromtimestamp(close_timestamp, tz=timezone.utc)
        if timestamp == close_ts:
            return close
    return None
