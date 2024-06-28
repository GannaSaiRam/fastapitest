from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel

from utils.enum import Status
from schemas.base import BaseSchema


class BatchGroupCreate(BaseSchema):
    parent_id: Optional[int] = None
    name: str
    status: str = Status.STARTED
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    attr_1_key: Optional[str] = None
    attr_1_value: Optional[str] = None
    attr_2_key: Optional[str] = None
    attr_2_value: Optional[str] = None
    attr_3_key: Optional[str] = None
    attr_3_value: Optional[str] = None
    attr_4_key: Optional[str] = None
    attr_4_value: Optional[str] = None
    attr_5_key: Optional[str] = None
    attr_5_value: Optional[str] = None
    attr_6_key: Optional[str] = None
    attr_6_value: Optional[str] = None


class BatchGroupUpdate(BaseModel):
    status: str
    updated_at: datetime = datetime.utcnow()


class BatchGroupResponse(BaseSchema):
    name: Optional[str]
    parent_id: Optional[int]
    status: Optional[str]
    created_at: datetime
    updated_at: datetime
    attr_1_key: Optional[str]
    attr_1_value: Optional[str]
    attr_2_key: Optional[str]
    attr_2_value: Optional[str]
    attr_3_key: Optional[str]
    attr_3_value: Optional[str]
    attr_4_key: Optional[str]
    attr_4_value: Optional[str]
    attr_5_key: Optional[str]
    attr_5_value: Optional[str]
    attr_6_key: Optional[str]
    attr_6_value: Optional[str]

    class Config:
        orm_mode = True
