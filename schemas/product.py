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
    pass


class ProductResponse(ProductBase):
    id: UUID

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    id: UUID
    sku: str
    name: str
    price: float
