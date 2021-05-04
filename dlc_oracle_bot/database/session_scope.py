from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, ProgrammingError
from sqlalchemy.orm import sessionmaker

from dlc_oracle_bot.database.db_url import db_url


@contextmanager
def session_scope(echo=False,
                  raise_integrity_error=True,
                  raise_programming_error=True):
    """Provide a transactional scope around a series of operations."""
    engine = create_engine(db_url, echo=echo)
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    try:
        yield session
        session.commit()
    except IntegrityError:
        session.rollback()
        if raise_integrity_error:
            raise
    except ProgrammingError:
        session.rollback()
        if raise_programming_error:
            raise
    except:
        session.rollback()
        raise
    finally:
        session.close()
