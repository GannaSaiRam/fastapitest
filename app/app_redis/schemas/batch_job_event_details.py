from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from utils.enum import Status


class BatchJobEventDetailsCreate(BaseModel):
    batch_job_event_id: int
    event: str   # TODO: use ENUM for this
    status: str = Status.STARTED
    created_at: datetime = datetime.utcnow()


class BatchJobEventDetailsUpdate(BaseModel):
    status: str


class BatchJobEventDetailsResponse(BaseModel):
    batch_job_event_id: Optional[int]
    event: Optional[str]
    status: Optional[str]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
