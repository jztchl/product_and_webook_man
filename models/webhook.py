from sqlalchemy import Column, String, Boolean, Text, Float
from database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Webhook(Base):
    __tablename__ = "webhooks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = Column(String(500), nullable=False)
    event_type = Column(String(50))
    active = Column(Boolean, default=True)

