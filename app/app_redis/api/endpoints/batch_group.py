from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.background import BackgroundTasks

from crud import BatchGroupCRUD, CRUDException
from db import get_session
from post_request_bodies import SequenceFormatBody
from schemas import BatchGroupCreate, BatchGroupUpdate, BatchGroupResponse

router = APIRouter()
CRUDInstance = BatchGroupCRUD()


@router.post("/sequence")
async def get_next_sequences(
        *,
        sequence_dict: SequenceFormatBody = None
):
    out = await CRUDInstance.get_next_sequence_value(sequence_dict=sequence_dict)
    return out


@router.post("", response_model=dict)
async def create_batch_group(
        *,
        batch_group: BatchGroupCreate,
        background_tasks: BackgroundTasks,
):
    now_time = datetime.utcnow()
    batch_group.created_at = now_time
    batch_group.updated_at = now_time
    field_types = {}
    for f, v in BatchGroupCreate.__fields__.items():
        field_types[f] = v.annotation
    try:
        CRUDInstance.create(data=batch_group, field_types=field_types, background_tasks=background_tasks)
    except CRUDException as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {
        "status": "Raised request to insert group record for given id",
    }


@router.get("/{_id}", response_model=BatchGroupResponse)
async def retrieve_batch_group(
        *,
        _id: int,
        db: AsyncSession = Depends(get_session),
):
    batch_group_pg = await CRUDInstance.get_by_id_pg(_id=_id, async_session=db)
    if batch_group_pg is None:
        batch_group = {}
    else:
        batch_group = batch_group_pg.__dict__
    batch_group_rs: dict = await CRUDInstance.get_by_id_rs(_id=_id)
    batch_group.update(batch_group_rs)
    if not batch_group:
        raise HTTPException(status_code=404, detail="Batch group not found")
    return BatchGroupResponse.parse_obj(batch_group)


@router.put("/{_id}", response_model=dict)
async def update_batch_group_status(
        *,
        _id: int,
        batch_group_input: BatchGroupUpdate,
        background_tasks: BackgroundTasks,
):
    batch_group_input.updated_at = datetime.utcnow()
    field_types = {}
    for f, v in BatchGroupUpdate.__fields__.items():
        field_types[f] = v.annotation
    try:
        CRUDInstance.update_status(
            _id=_id, data=batch_group_input, status=batch_group_input.status, background_tasks=background_tasks,
            field_types=field_types,
        )
    except CRUDException as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {
        "status": "Raised request to update group record for given id",
    }
