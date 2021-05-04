import os
import time

from alembic import context, script, command
from alembic.config import Config
from alembic.runtime import migration
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError

from dlc_oracle_bot.database.base import Base
from dlc_oracle_bot.database.db_url import db_url
from dlc_oracle_bot.database.session_scope import session_scope
from dlc_oracle_bot.logging_utility import log

target_metadata = Base.metadata
import dlc_oracle_bot.models

this_file_path = os.path.realpath(__file__)
database_directory_path = os.path.dirname(this_file_path)
config_path = os.path.join(database_directory_path, 'alembic.ini')


def get_current_head(connectable: Engine) -> set:
    with connectable.begin() as connection:
        context = migration.MigrationContext.configure(connection)
        current_head = set(context.get_current_heads())
        return current_head


def create_or_update_database(echo=True):

    alembic_config = Config(config_path)

    try:
        with session_scope(echo=echo) as session:
            directory = script.ScriptDirectory.from_config(alembic_config)
            get_head = set(directory.get_heads())
            current_head = get_current_head(connectable=session.bind.engine)
            if current_head == get_head:
                return
            elif not current_head:
                Base.metadata.create_all(session.connection())
                command.stamp(alembic_config, 'head')
            else:
                command.upgrade(alembic_config, 'head')

    except OperationalError as e:
        log.error('OperationalError in create_or_update_database', e=e, exc_info=True)
        time.sleep(10)
        create_or_update_database(echo=echo)


def run_migrations():
    engine = create_engine(db_url)

    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
