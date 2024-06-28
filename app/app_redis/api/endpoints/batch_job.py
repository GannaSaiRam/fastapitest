from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.background import BackgroundTasks

from crud import BatchJobCRUD, CRUDException
from db import get_session
from post_request_bodies import SequenceFormatBody
from schemas import BatchJobCreate, BatchJobUpdate, BatchJobResponse

router = APIRouter()
CRUDInstance = BatchJobCRUD()


@router.post("/sequence")
async def get_next_sequences(
        *,
        sequence_dict: SequenceFormatBody = None
):
    out = await CRUDInstance.get_next_sequence_value(sequence_dict=sequence_dict)
    return out


@router.post("", response_model=dict)
async def create_batch_job(
        *,
        batch_job: BatchJobCreate,
        background_tasks: BackgroundTasks,
):
    now_time = datetime.utcnow()
    batch_job.created_at = now_time
    batch_job.updated_at = now_time
    field_types = {}
    for f, v in BatchJobCreate.__fields__.items():
        field_types[f] = v.annotation
    try:
        CRUDInstance.create(data=batch_job, field_types=field_types, background_tasks=background_tasks)
    except CRUDException as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {
        "status": "Raised request to insert job record for given id",
    }


@router.get("/{_id}", response_model=BatchJobResponse)
async def retrieve_batch_job(
        *,
        _id: int,
        db: AsyncSession = Depends(get_session),
):
    batch_job_pg = await CRUDInstance.get_by_id_pg(_id=_id, async_session=db)
    if batch_job_pg is None:
        batch_job = {}
    else:
        batch_job = batch_job_pg.__dict__
    batch_job_rs: dict = await CRUDInstance.get_by_id_rs(_id=_id)
    batch_job.update(batch_job_rs)
    if not batch_job:
        raise HTTPException(status_code=404, detail="Batch job not found")
    return BatchJobResponse.parse_obj(batch_job)


@router.put("/{_id}", response_model=dict)
async def update_batch_job_status(
        *,
        _id: int,
        batch_job_input: BatchJobUpdate,
        background_tasks: BackgroundTasks,
):
    batch_job_input.updated_at = datetime.utcnow()
    field_types = {}
    for f, v in BatchJobUpdate.__fields__.items():
        field_types[f] = v.annotation
    try:
        CRUDInstance.update_status(
            _id=_id, data=batch_job_input, status=batch_job_input.status, background_tasks=background_tasks,
            field_types=field_types,
        )
    except CRUDException as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {
        "status": "Raised request to update job record for given id",
    }
