from pydantic import BaseModel

class StatusUpdate(BaseModel):
    status: bool