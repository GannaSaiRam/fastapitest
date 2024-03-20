from fastapi import APIRouter

from app.api.endpoints import (
    batch_group_router,
    batch_job_router,
    batch_job_details_router,
    batch_job_event_details_router,
    normal_router,
)

api_router = APIRouter()
api_router.include_router(normal_router, prefix="")
api_router.include_router(batch_group_router, prefix="/batch_group", tags=["batch-group"])
api_router.include_router(batch_job_router, prefix="/batch-job", tags=["batch-job"])
api_router.include_router(batch_job_details_router, prefix="/batch-job-details", tags=["batch-job-details"])
api_router.include_router(
    batch_job_event_details_router, prefix="/batch-job-event-details", tags=["batch-job-event-details"]
)
