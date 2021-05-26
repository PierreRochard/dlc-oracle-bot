from datetime import datetime, timezone, timedelta
import os
from pprint import pformat

from dotenv import load_dotenv

from dlc_oracle_bot.external_rate_services.cryptowatch_rates import get_daily_close
from dlc_oracle_bot.oracle.generate_price_image import generate_price_image
from dlc_oracle_bot.oracle.oracle_client import OracleClient
from dlc_oracle_bot.oracle.generate_announcement_image import generate_announcement_image

load_dotenv()


class Announcer(object):
    def __init__(self):
        self.oracle_client = OracleClient(host=os.environ['ORACLE_SERVER_HOST'],
                                          port=int(os.environ['ORACLE_SERVER_PORT']))

    @staticmethod
    def get_label(source: str, exchange: str, pair: str, close_timestamp: datetime):
        return f'{source}-{exchange}-{pair}-{close_timestamp.isoformat()}'

    @staticmethod
    def parse_label(label: str):
        split_label = label.split('-')
        return {
            'source': split_label.pop(0),
            'exchange': split_label.pop(0),
            'pair': split_label.pop(0),
            'close_timestamp': '-'.join(split_label)
        }

    def request_announcement(self, pair: str, timestamp: float, source: str = 'cryptowatch', exchange: str = 'kraken'):
        minimum = 0
        maximum = 1000000
        precision = 0

        datetime_requested = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        datetime_requested_truncated = datetime_requested.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        label = self.get_label(
            source=source,
            exchange=exchange,
            pair=pair,
            close_timestamp=datetime_requested_truncated
        )

        announcement = self.oracle_client.get_event(label=label)
        if announcement is None and datetime_requested_truncated > datetime.now(tz=timezone.utc):
            self.oracle_client.create_event(
                label=label,
                maturation=datetime_requested_truncated,
                minimum=minimum,
                maximum=maximum,
                unit=pair,
                precision=precision
            )
            announcement = self.oracle_client.get_event(label=label)

        if announcement is not None and announcement['signed_outcome'] is None \
                and datetime_requested_truncated < datetime.now(tz=timezone.utc):
            close = get_daily_close(timestamp=datetime_requested_truncated, exchange=exchange, pair=pair)
            if close is not None:
                self.oracle_client.sign_event(label=label, value=close)
                announcement = self.oracle_client.get_event(label=label)
        return announcement


if __name__ == '__main__':
    today = datetime.now(tz=timezone.utc)
    tomorrow = today + timedelta(days=1)
    days = [today, tomorrow]
    for i in range(1, 10):
        historical_day = today - timedelta(days=i)
        days.insert(0, historical_day)
    announcements = []
    announcer = Announcer()
    for i, day in enumerate(days):
        announced = announcer.request_announcement('BTCUSD', day.timestamp())
        announcements.append(announced)
        if announced is not None and announced.get('signed_outcome', None) is not None:
            parsed_label = announcer.parse_label(announced['label'])
            previous_day = day - timedelta(days=1)
            previous_day_close = get_daily_close(timestamp=previous_day,
                                                 exchange=parsed_label['exchange'],
                                                 pair=parsed_label['pair'])
            generate_price_image(
                today_price=announced['signed_outcome'],
                yesterdays_price=previous_day_close,
                today_date=announced['maturation_time'],
                pair=parsed_label['pair']
            )
        if announced is not None and announced.get('attestations', None) is not None:
            generate_announcement_image(
                attestations=announced['attestations'],
                price=announced['signed_outcome'],
                pair=announcer.parse_label(announced['label'])['pair'],
                exchange=announcer.parse_label(announced['label'])['exchange'],
                maturation_time=announced['maturation_time']
            )

    print(pformat(announcements))
