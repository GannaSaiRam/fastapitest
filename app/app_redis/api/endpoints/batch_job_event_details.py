from datetime import datetime

from fastapi import APIRouter, HTTPException
from starlette.background import BackgroundTasks

from crud import BatchJobEventDetailsCRUD, CRUDException
from schemas import BatchJobEventDetailsCreate, BatchJobEventDetailsUpdate

router = APIRouter()
CRUDInstance = BatchJobEventDetailsCRUD()


# @router.get("/sequence", response_model=dict)
async def get_next_sequence():
    return {"nextSequence": await CRUDInstance.get_next_sequence_value()}


@router.post("", response_model=dict)
async def create_batch_job_event_details(
        *,
        batch_job_event_details: BatchJobEventDetailsCreate,
        background_tasks: BackgroundTasks,
):
    batch_job_event_details.created_at = datetime.utcnow()
    field_types = {}
    for f, v in BatchJobEventDetailsCreate.__fields__.items():
        field_types[f] = v.annotation
    try:
        CRUDInstance.create(
            data=batch_job_event_details, field_types=field_types, uniques=("batch_job_event_id", "status"),
            background_tasks=background_tasks
        )
    except CRUDException as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {
        "status": "Raised request to insert event detail record for given id",
    }


# @router.put("/{_id}", response_model=dict)
async def update_batch_job_event_details_status(
        *,
        _id: int,
        batch_job_event_details_input: BatchJobEventDetailsUpdate,
        background_tasks: BackgroundTasks,
):
    field_types = {}
    for f, v in BatchJobEventDetailsUpdate.__fields__.items():
        field_types[f] = v.annotation
    try:
        CRUDInstance.update_status(
            _id=_id, status=batch_job_event_details_input.status, background_tasks=background_tasks,
            field_types=field_types
        )
    except CRUDException as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {
        "status": "Raised request to update event detail record for given id",
    }
