import uuid
import shutil
from fastapi import APIRouter, UploadFile, HTTPException, Request
from workers.tasks import import_csv_task
from redis import Redis
from config import settings
import logging
import os 
from fastapi import File 
from enums import ImportStatus

router = APIRouter(prefix="/upload", tags=["upload"])

try:
    redis_client = Redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,
        socket_connect_timeout=5,
        socket_timeout=5,
        retry_on_timeout=True,
        health_check_interval=30,
    )
except Exception as e:
    logging.error(f"Failed to connect to Redis: {e}")
    raise RuntimeError("Failed to connect to Redis")


@router.post("/")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    task_id = str(uuid.uuid4())

    folder_path = os.path.join("tmp")
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, f"{task_id}.csv")
    with open(file_path, "wb") as f:
        while chunk := await file.read(8192):
            f.write(chunk)

    redis_client.hset(f"progress:{task_id}", mapping={
        "percent": 0,
        "status": ImportStatus.QUEUED.value,
        "processed": 0
    })

    import_csv_task.delay(file_path, task_id)

    return {"task_id": task_id}
