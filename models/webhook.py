from sqlalchemy import Column, String, Boolean, Text, Float, DateTime
from database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class Webhook(Base):
    __tablename__ = "webhooks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = Column(String(500), nullable=False)
    event_type = Column(String(50))
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())

