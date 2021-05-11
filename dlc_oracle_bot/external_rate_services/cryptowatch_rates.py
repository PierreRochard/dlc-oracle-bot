from datetime import datetime
import os

import cryptowatch as cw
from dotenv import load_dotenv
from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound

from dlc_oracle_bot.database.session_scope import session_scope
from dlc_oracle_bot.logging_utility import log
from dlc_oracle_bot.models import Sources, Pairs

load_dotenv()

cw.api_key = os.environ['CRYPTOWATCH_PUBLIC_KEY']


class CryptowatchRates(object):
    def populate_sources(self):
        with session_scope() as session:
            try:
                source = session.query(Sources).filter(Sources.exchange == 'kraken').one()
            except NoResultFound:
                source = Sources()
                source.exchange = 'kraken'
                source.data_provider = 'cryptowatch'
                session.add(source)

    def populate_pairs(self, exchange: str = 'kraken'):
        exchange = cw.markets.list(exchange)
        markets = exchange.markets

        with session_scope() as session:
            source = session.query(Sources).filter(Sources.label == exchange).one()
            for market in markets:
                if not market.active:
                    continue

                pair_name = market.pair.upper()
                try:
                    pair_record = session.query(Pairs).filter(
                        and_(
                            Pairs.source_id == source.id,
                            Pairs.name == pair_name
                        )
                    ).one()
                except NoResultFound:
                    pair_record = Pairs()
                    pair_record.source_id = source.id
                    pair_record.name = pair_name
                    session.add(pair_record)

    def get_close(self, timestamp: datetime, exchange: str, pair: str):
            ticker = "{}:{}".format(exchange, pair).upper()
            candles = cw.markets.get(ticker, ohlc=True, periods=['1d'])
            candles = [candles.of_1d[-1]]
            for candle in candles:
                log.debug('candle', candle=candle)
                close_timestamp, open_px, high, low, close, volume, volume_quote = candle
                close_ts = datetime.utcfromtimestamp(close_timestamp)
                if timestamp == close_ts:
                    return close
            return None


if __name__ == '__main__':
    CryptowatchRates().populate_Pairs()