from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_batch_job():
    return {"Message": "Hello from Batch Job"}
