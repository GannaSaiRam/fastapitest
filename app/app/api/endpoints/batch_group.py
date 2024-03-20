from fastapi import APIRouter


router = APIRouter()

@router.get("/")
def get_batch_group():
    return {"Message": "Hello from Batch Group"}
