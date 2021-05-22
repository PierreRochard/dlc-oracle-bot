from datetime import datetime, timezone, timedelta
import os
from pprint import pformat

from dotenv import load_dotenv

from dlc_oracle_bot.external_rate_services.cryptowatch_rates import get_close
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
            close = get_close(timestamp=datetime_requested_truncated, exchange=exchange, pair=pair)
            if close is not None:
                self.oracle_client.sign_event(label=label, value=close)
                announcement = self.oracle_client.get_event(label=label)
        return announcement


if __name__ == '__main__':
    today = datetime.utcnow()
    tomorrow = today + timedelta(days=1)
    days = [today, tomorrow]
    for i in range(1, 10):
        historical_day = today - timedelta(days=i)
        days.insert(0, historical_day)
    announcements = []
    for i, day in enumerate(days):
        announced = Announcer().request_announcement('BTCUSD', day.timestamp())
        announcements.append(announced)
        if i > 0:
            previous_day_announcement = announcements[i -1]
        else:
            previous_day_announcement = None
        if announced is not None and previous_day_announcement is not None:
            generate_price_image(announced, previous_day_announcement)
        if announced is not None and announced.get('attestations', None) is not None:
            generate_announcement_image(announced)
    print(pformat(announcements))
