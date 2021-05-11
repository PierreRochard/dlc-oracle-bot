import uuid

from sqlalchemy import (
    Column,
    DateTime,
    func,
    Numeric,
    Text, JSON
)

from dlc_oracle_bot.database.base import Base
from dlc_oracle_bot.models.guid import GUID


class PriceAnnouncements(Base):
    __tablename__ = 'price_announcements'

    created_at = Column(DateTime(timezone=True),
                        nullable=False,
                        server_default=func.now())

    updated_at = Column(DateTime(timezone=True),
                        onupdate=func.now(),
                        server_default=func.now())

    deleted_at = Column(DateTime(timezone=True))

    id = Column(
        GUID,
        primary_key=True,
        default=uuid.uuid4
    )
    asset_id = Column(GUID)
    period = Column(Text)
    close_timestamp = Column(DateTime(timezone=True))
    signed_outcome = Column(Numeric)
    announcement_tlv = Column(Text)
    maturation_time_epoch = Column(Numeric)
    announcement_signature = Column(Text)
    signing_version = Column(Text)
    event_tlv = Column(Text)
    maturation_time = Column(DateTime(timezone=True))
    nonces = Column(JSON)
    outcomes = Column(JSON)
    label = Column(Text)
    event_descriptor_tlv = Column(Text)
    attestations = Column(Text)
