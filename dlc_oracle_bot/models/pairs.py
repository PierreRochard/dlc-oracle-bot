import uuid

from sqlalchemy import (
    Column,
    DateTime,
    func,
    Text
)

from dlc_oracle_bot.database.base import Base
from dlc_oracle_bot.models.guid import GUID


class Pairs(Base):
    __tablename__ = 'pairs'

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
    source_id = Column(GUID)
    name = Column(Text)
