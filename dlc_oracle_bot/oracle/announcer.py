from datetime import datetime, timezone, timedelta
import os

from dotenv import load_dotenv

from dlc_oracle_bot.external_rate_services.cryptowatch_rates import get_close
from dlc_oracle_bot.oracle.oracle_client import OracleClient

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
        if announcement is None:
            self.oracle_client.create_event(
                label=label,
                maturation=datetime_requested_truncated,
                minimum=minimum,
                maximum=maximum,
                unit=pair,
                precision=precision
            )
            announcement = self.oracle_client.get_event(label=label)

        if datetime_requested_truncated < datetime.utcnow():
            close = get_close(timestamp=datetime_requested_truncated, exchange=exchange, pair=pair)
            if close is not None:
                self.oracle_client.sign_event(label=label, value=close)
                announcement = self.oracle_client.get_event(label=label)
        return announcement


if __name__ == '__main__':
    today = datetime.utcnow()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    for day in [yesterday, today, tomorrow]:
        announced = Announcer().request_announcement('BTCUSD', day.timestamp())
        print(announced)
