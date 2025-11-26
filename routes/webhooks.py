from fastapi import APIRouter

router = APIRouter()

@router.post("/webhooks")
def create_webhook():
    return {"message": "Webhook created"}