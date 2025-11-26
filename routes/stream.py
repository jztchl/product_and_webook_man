from fastapi import APIRouter
from redis import Redis
from config import settings
from fastapi.responses import StreamingResponse
import asyncio
import json
from enums import ImportStatus
router = APIRouter(prefix="/stream", tags=["progress"])

redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)


async def progress_stream(task_id: str):
    key = f"progress:{task_id}"

    while True:
        data = redis.hgetall(key)
        if not data:
            yield f"data: {json.dumps({'error': 'invalid task id'})}\n\n"
            break

        yield f"data: {json.dumps(data)}\n\n"

        if data.get("status") == ImportStatus.COMPLETED.value or data.get("status") == ImportStatus.FAILED.value:
            break

        await asyncio.sleep(1)


@router.get("/progress/{task_id}")
async def stream_progress(task_id: str):
    return StreamingResponse(progress_stream(task_id), media_type="text/event-stream")
