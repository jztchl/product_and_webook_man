from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from enums import WebhookEvent
from pydantic import field_validator, Field

class WebhookBase(BaseModel):
    url: str
    event_type: Optional[str] = Field(
        None,
        description="Type of event to listen for",
        json_schema_extra={
            "example": WebhookEvent.PRODUCT_CREATED.value,
            "enum": [e.value for e in WebhookEvent]
        }
    )
    active: bool = True
    created_at: Optional[datetime] = None

    @field_validator("event_type")
    def validate_event_type(cls, v):
        if v not in [e.value for e in WebhookEvent]:
            raise ValueError(f"Invalid event type: {v}")
        return v

class WebhookCreate(WebhookBase):
    pass

class WebhookUpdate(WebhookBase):
    pass
    class Config:
        from_attributes = True

class WebhookResponse(WebhookBase):
    id: UUID
    class Config:
        from_attributes = True
