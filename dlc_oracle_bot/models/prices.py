import uuid

from sqlalchemy import (
    Column,
    DateTime,
    func,
    Numeric
)

from dlc_oracle_bot.database.base import Base
from dlc_oracle_bot.models.guid import GUID


class Prices(Base):
    __tablename__ = 'prices'

    created_at = Column(DateTime(timezone=True),
                        nullable=False,
                        server_default=func.now())

    updated_at = Column(DateTime(timezone=True),
                        nullable=False,
                        onupdate=func.now(),
                        server_default=func.now())

    deleted_at = Column(DateTime(timezone=True),
                        nullable=True)

    id = Column(
        GUID,
        primary_key=True,
        default=uuid.uuid4
    )
    asset_id = Column(GUID)
    rate = Column(Numeric)
