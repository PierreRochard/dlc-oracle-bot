from datetime import datetime, timedelta
import os

from dotenv import load_dotenv
from dateutil.relativedelta import relativedelta, TH

from dlc_oracle_bot.external_rate_services.timeframes import timeframes

# Announcer is a service that queries the rates database and creates announcements
from dlc_oracle_bot.oracle.oracle_client import OracleClient


class Announcer(object):
    def __init__(self):
        load_dotenv()
        self.oracle_client = OracleClient(host=os.environ['ORACLE_SERVER_HOST'],
                                          port=int(os.environ['ORACLE_SERVER_PORT']))

    @staticmethod
    def get_label(source: str, venue: str, asset_name: str, unit_of_account: str, close_timestamp: datetime):
        return f'{source}-{venue}-{asset_name}-{unit_of_account}-{close_timestamp.isoformat()}'

    def generate_future_announcements(self):
        source = 'cryptowatch'
        venue = 'kraken'
        asset_name = 'BTC'
        unit_of_account = 'EUR'
        minimum = 0
        maximum = 1000000
        precision = 0

        weekly_timeframe = timeframes[0]
        now = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        this_week_close_timestamp = now + relativedelta(weekday=TH)
        close_timestamps = [this_week_close_timestamp]
        for week in range(1, 10):
            weekly_timestamp = this_week_close_timestamp + timedelta(days=weekly_timeframe.days * week)
            close_timestamps.append(weekly_timestamp)

        announcements = []
        for close_timestamp in close_timestamps:
            label = self.get_label(source=source, venue=venue, asset_name=asset_name, unit_of_account=unit_of_account,
                                   close_timestamp=close_timestamp)
            existing_announcement = self.oracle_client.get_event(label=label)
            if existing_announcement is not None:
                announcements.append(existing_announcement)
            else:
                self.oracle_client.create_event(label=label, maturation=close_timestamp,
                                                                   minimum=minimum, maximum=maximum,
                                                                   unit=unit_of_account, precision=precision)
                new_announcement = self.oracle_client.get_event(label=label)
                announcements.append(new_announcement)
        print('here')



    def sign_past_announcements(self):
        pass


if __name__ == '__main__':
    Announcer().generate_future_announcements()
