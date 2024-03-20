from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def get_normal():
    return {"Message": "Hello from Code"}
