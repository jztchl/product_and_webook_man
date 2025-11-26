from enum import Enum


class WebhookEvent(Enum):
    PRODUCT_CREATED = "product_created"
    PRODUCT_UPDATED = "product_updated"
    PRODUCT_DELETED = "product_deleted"
    PRODUCT_DELETED_ALL = "product_deleted_all"
    PRODUCT_IMPORTED = "product_imported"



class ImportStatus(Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"