from sqlalchemy import Column, String, Boolean, Text, Float
from database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Product(Base):
    __tablename__ = "product"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sku = Column("sku", String(255), unique=True, nullable=False)
    description = Column("description", Text)
    price = Column("price", Float)
    active = Column("active", Boolean, default=True)

