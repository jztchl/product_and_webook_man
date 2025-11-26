from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class ProductBase(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    price: Optional[float] = None
    active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    sku:Optional[str] = None
    active:Optional[bool] = None


class ProductResponse(ProductBase):
    id: UUID

    class Config:
        from_attributes = True

