from sqlalchemy.dialects.postgresql import insert
from database import SessionLocal
from models.product import Product
from redis import Redis
from config import settings
import csv
from .celery_app import celery_app
import os
import logging
from enums import ImportStatus, WebhookEvent

redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)

BATCH_SIZE = 2000  


@celery_app.task
def import_csv_task(file_path: str, task_id: str):
    redis.hset(f"progress:{task_id}", "status", ImportStatus.PROCESSING.value)
    processed = 0

    try:
      
        with open(file_path, "r") as f:
            total_rows = sum(1 for _ in f)

        batch = []

        with SessionLocal() as db:
            with open(file_path, "r") as f:
                reader = csv.DictReader(f)

                for row in reader:
                    processed += 1

                    batch.append({
                        "sku": row.get("sku", "").lower().strip(),
                        "name": row.get("name", "").lower().strip(),
                        "description": row.get("description"),
                        "price": float(row.get("price") or 0),
                        "active": True
                    })

                    
                    if len(batch) >= BATCH_SIZE:
                        flush_batch(db, batch)
                        batch.clear()


                    if processed % 1000 == 0:
                        percent = int((processed / total_rows) * 100)
                        redis.hset(f"progress:{task_id}", mapping={
                            "percent": percent,
                            "status": ImportStatus.PROCESSING.value,
                            "processed": processed,
                        })

                if batch:
                    flush_batch(db, batch)

                db.commit()

        redis.hset(f"progress:{task_id}", mapping={
            "percent": 100,
            "status": ImportStatus.COMPLETED.value,
            "processed": processed
        })

    except Exception as e:
        logging.error(f"Error importing CSV: {e}")
        redis.hset(f"progress:{task_id}", mapping={
            "percent": 100,
            "status": ImportStatus.FAILED.value,
            "processed": processed,
        })

    finally:
        redis.expire(f"progress:{task_id}", 1200)
        if os.path.exists(file_path):
            os.remove(file_path)
            logging.info(f"file removed {file_path}")

    return "completed"


def flush_batch(db, batch):
    stmt = insert(Product.__table__).values(batch)

    stmt = stmt.on_conflict_do_update(
        index_elements=[Product.sku],
        set_={
            "description": stmt.excluded.description,
            "price": stmt.excluded.price,
            "active": True,
        }
    )

    db.execute(stmt)




@celery_app.task
def deliver_webhook(event_type: str, payload: dict):
    from models.webhook import Webhook
    from database import SessionLocal
    import httpx, time, logging

    with SessionLocal() as db:
        webhooks = db.query(Webhook).filter_by(event_type=event_type, active=True).all()

    for hook in webhooks:
        try:
            start = time.time()
            res = httpx.post(hook.url, json=payload, timeout=5)
            logging.info(
                f"[Webhook] Delivered to {hook.url} ({event_type}) - "
                f"{res.status_code} in {int((time.time() - start)*1000)}ms"
            )
        except Exception as e:
            logging.error(f"[Webhook ERROR] {hook.url}: {e}")
