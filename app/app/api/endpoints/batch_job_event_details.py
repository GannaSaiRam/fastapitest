from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_batch_job_event_details():
    return {"Message": "Hello from Batch Job Event Details"}
