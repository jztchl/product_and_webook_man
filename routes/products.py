from fastapi import APIRouter

router = APIRouter()

@router.post("/products/import")
def import_products():
    return {"message": "Import started"}