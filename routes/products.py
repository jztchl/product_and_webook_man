from fastapi import APIRouter
from sqlalchemy.orm import Session
from models.product import Product
from database import get_db
from fastapi import Depends
from schemas.product import ProductCreate, ProductUpdate, ProductResponse
import uuid 
from typing import Optional
import logging
from workers.tasks import deliver_webhook
from enums import WebhookEvent
import datetime
router = APIRouter(prefix="/products")



@router.post("/create", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        db_product = db.query(Product).filter_by(sku=product.sku).first()
        if db_product:
            return {"message": "Product already exists"}
        db_product = Product(**product.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        logging.info(f"Product created: {db_product.name}")
        payload = {
            "sku": db_product.sku,
            "name": db_product.name,
            "description": db_product.description,
            "price": db_product.price,
            "active": db_product.active,
            "created_at": str(datetime.datetime.now())
        }
        deliver_webhook.delay(WebhookEvent.PRODUCT_CREATED.value, payload)
        return db_product
    except Exception as e:
        logging.error(f"Error creating product: {e}")
        return {"message": str(e)}

@router.get("/list", response_model=list[ProductResponse])
def list_products(
    skip: int = 0, 
    limit: int = 100, 
    sku: Optional[str] = None, 
    name: Optional[str] = None, 
    active: Optional[bool] = None, 
    description: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    if sku:
        query = query.filter(Product.sku.ilike(f"%{sku}%"))
    if name:
        query = query.filter(Product.description.ilike(f"%{name}%"))
    if active is not None:
        query = query.filter(Product.active == active)
    if description:
        query = query.filter(Product.description.ilike(f"%{description}%"))
    return query.offset(skip).limit(limit).all()

@router.get("/get/{product_id}", response_model=ProductResponse)
def get_product(product_id: str, db: Session = Depends(get_db)):
    try:
        db_product = db.query(Product).get(uuid.UUID(product_id))
        return db_product
    except ValueError:
        logging.error(f"Product not found: {product_id}")
        return {"message": "Product not found"}

from pydantic import BaseModel

class StatusUpdate(BaseModel):
    status: bool

@router.post("/set_status/{product_id}", response_model=ProductResponse)
def set_product_active(product_id: str, status_update: StatusUpdate, db: Session = Depends(get_db)):
    try:
        db_product = db.query(Product).get(uuid.UUID(product_id))
        db_product.active = status_update.status
        db.commit()
        db.refresh(db_product)
        return db_product
    except ValueError:
        logging.error(f"Product not found: {product_id}")
        return {"message": "Product not found"}

@router.put("/update/{product_id}", response_model=ProductResponse)
def update_product(product_id: str, product: ProductUpdate, db: Session = Depends(get_db)):
    try:
        db_product = db.query(Product).get(uuid.UUID(product_id))
        for field, value in product.model_dump(exclude_unset=True).items():
            setattr(db_product, field, value)
        db.commit()
        db.refresh(db_product)
        payload = {
            "sku": db_product.sku,
            "name": db_product.name,
            "description": db_product.description,
            "price": db_product.price,
            "active": db_product.active,
            "updated_at": str(datetime.datetime.now())
        }
        deliver_webhook.delay(WebhookEvent.PRODUCT_UPDATED.value, payload)
        return db_product
    except ValueError:
        logging.error(f"Product not found: {product_id}")
        return {"message": "Product not found"}


@router.delete("/delete/delete_all")
def delete_all_products(msg:str ,db: Session = Depends(get_db)):
    try:
        if msg != "delete all products":
            return {"message": "Invalid message"}
        db.query(Product).delete()
        db.commit()
        payload = {
            "message": "All products deleted",
            "deleted_at": str(datetime.datetime.now())
        }
        deliver_webhook.delay(WebhookEvent.PRODUCT_DELETED_ALL.value, payload)
        logging.info("All products deleted")
        return {"message": "All products deleted"}
    except Exception as e:
        logging.error(f"Error deleting all products: {e}")
        return {"message": str(e)}


@router.delete("/delete/{product_id}")
def delete_product(product_id: str, db: Session = Depends(get_db)):
    try:
        db_product = db.query(Product).get(uuid.UUID(product_id))
        db.delete(db_product)
        db.commit()
        payload = {
            "sku": db_product.sku,
            "name": db_product.name,
            "description": db_product.description,
            "price": db_product.price,
            "active": db_product.active,
            "deleted_at": str(datetime.datetime.now())
        }
        deliver_webhook.delay(WebhookEvent.PRODUCT_DELETED.value, payload)
        logging.info("Product deleted")
        return {"message": "Product deleted"}
    except ValueError:
        logging.error(f"Product not found: {product_id}")
        return {"message": "Product not found"}


