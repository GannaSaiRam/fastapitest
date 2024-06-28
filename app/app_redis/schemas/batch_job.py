from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from schemas.base import BaseSchema
from utils.enum import Status


class BatchJobCreate(BaseSchema):
    batch_group_id: int
    name: str
    description: str = None
    processing_env: str
    status: str = Status.STARTED
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()


class BatchJobUpdate(BaseModel):
    status: str
    updated_at: datetime = datetime.utcnow()


class BatchJobResponse(BaseSchema):
    batch_group_id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    processing_env: Optional[str]
    status: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

