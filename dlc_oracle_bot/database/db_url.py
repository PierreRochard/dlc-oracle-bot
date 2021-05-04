import os

from sqlalchemy.engine import URL

import dotenv

from dlc_oracle_bot.logging_utility import log

dotenv.load_dotenv()

db_url = URL(
    drivername=os.environ['DB_DRIVER'],
    host=os.environ['DB_HOST'],
    port=os.environ['DB_PORT'],
    username=os.environ['DB_USER'],
    password=os.environ['DB_PASSWORD'],
    database=os.environ['DB_DATABASE']
)

log.debug('db_url', db_url=db_url)
