from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from schemas.base import BaseSchema
from utils.enum import Status


class BatchJobEventsCreate(BaseSchema):
    batch_job_id: int
    event: str   # TODO: use ENUM for this
    status: str = Status.STARTED
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()


class BatchJobEventsUpdate(BaseModel):
    status: str
    updated_at: datetime = datetime.utcnow()


class BatchJobEventsResponse(BaseSchema):
    batch_job_id: Optional[int]
    event: Optional[str]
    status: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
