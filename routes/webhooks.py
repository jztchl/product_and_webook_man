from fastapi import APIRouter
from fastapi import APIRouter, HTTPException
from models.webhook import Webhook
from database import get_db
from fastapi import Depends
from schemas.webhook import WebhookCreate, WebhookUpdate, WebhookResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/webhooks")
@router.post("/create", response_model=WebhookResponse)
def create_webhook(webhook: WebhookCreate, db: Session = Depends(get_db)):
    db_webhook = db.query(Webhook).filter_by(url=webhook.url).first()
    if db_webhook:
        raise HTTPException(status_code=400, detail="Webhook already exists")
    webhook_model = Webhook(**webhook.model_dump())
    db.add(webhook_model)
    db.commit()
    db.refresh(webhook_model)
    return webhook_model

@router.get("/list", response_model=list[WebhookResponse])
def list_webhooks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Webhook).offset(skip).limit(limit).all()

@router.get("/get/{webhook_id}", response_model=WebhookResponse)
def get_webhook(webhook_id: str, db: Session = Depends(get_db)):
    webhook = db.query(Webhook).get(webhook_id)
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    return webhook

@router.put("/update/{webhook_id}", response_model=WebhookResponse)
def update_webhook(webhook_id: str, webhook_update: WebhookUpdate, db: Session = Depends(get_db)):
    db_webhook = db.query(Webhook).get(webhook_id)
    if not db_webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    update_data = webhook_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_webhook, field, value)
    
    db.commit()
    db.refresh(db_webhook)
    return db_webhook

@router.delete("/delete/{webhook_id}")
def delete_webhook(webhook_id: str, db: Session = Depends(get_db)):
    webhook = db.query(Webhook).get(webhook_id)
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    db.delete(webhook)
    db.commit()
    return {"message": "Webhook deleted"}


