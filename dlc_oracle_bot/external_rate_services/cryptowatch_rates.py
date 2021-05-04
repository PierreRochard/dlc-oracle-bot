import os

from datetime import datetime, timedelta


def main():
    import cryptowatch as cw

    from dotenv import load_dotenv
    from sqlalchemy import and_
    from sqlalchemy.exc import NoResultFound

    from dlc_oracle_bot.database.session_scope import session_scope
    from dlc_oracle_bot.logging_utility import log
    from dlc_oracle_bot.models import Sources, Assets, Prices
    load_dotenv()

    cw.api_key = os.environ['CRYPTOWATCH_PUBLIC_KEY']

    with session_scope() as session:
        try:
            source = session.query(Sources).filter(Sources.label == 'kraken').one()
        except NoResultFound:
            source = Sources()
            source.label = 'kraken'
            source.url = 'cryptowatch'
            session.add(source)

    # Get all Kraken markets
    kraken = cw.markets.list("kraken")
    markets = [kraken.markets[0]]

    # For each Kraken market...
    for market in markets:
        assert len(market.pair) == 6
        pair = market.pair.upper()
        asset_name, unit_of_account = pair[:3], pair[3:]

        with session_scope() as session:
            source = session.query(Sources).filter(Sources.label == 'kraken').one()
            try:
                asset = session.query(Assets).filter(
                    and_(
                        Assets.source_id == source.id,
                        Assets.name == asset_name,
                        Assets.unit_of_account == unit_of_account
                    )
                ).one()
            except NoResultFound:
                asset = Assets()
                asset.source_id = source.id
                asset.name = asset_name
                asset.unit_of_account = unit_of_account
                session.add(asset)

        ticker = "{}:{}".format(market.exchange, market.pair).upper()
        # Request weekly candles for that market
        candles = cw.markets.get(ticker, ohlc=True, periods=["1w"])
        candles = [candles.of_1w[-1]]
        for candle in candles:
            log.debug('candle', candle=candle)
            # Each candle is a list of [close_timestamp, open, high, low, close, volume, volume_quote]
            # Get close_timestamp, open and close from the most recent weekly candle
            close_ts, weekly_close = (
                datetime.utcfromtimestamp(candle[0]),
                candle[4],
            )
            open_ts = close_ts - timedelta(days=7)
            future_ts = close_ts + timedelta(days=7)
            with session_scope() as session:
                source = session.query(Sources).filter(Sources.label == 'kraken').one()
                asset = session.query(Assets).filter(
                    and_(
                        Assets.source_id == source.id,
                        Assets.name == asset_name,
                        Assets.unit_of_account == unit_of_account
                    )
                ).one()
                try:
                    price = session.query(Prices).filter(
                        and_(
                            Prices.asset_id == asset.id,
                            Prices.period == '1w',
                            Prices.close_timestamp == close_ts,
                        )
                    ).one()
                except NoResultFound:
                    price = Prices()
                    price.asset_id = asset.id
                    price.period = '1w'
                    price.close_timestamp = close_ts
                    price.rate = weekly_close
                    session.add(price)


if __name__ == '__main__':
    try:
        main()
    except ModuleNotFoundError as e:
        print(e)
        from dlc_oracle_bot.install_requirements import install_requirements

        install_requirements()
