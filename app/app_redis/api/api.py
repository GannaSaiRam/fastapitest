from fastapi import APIRouter

from api.endpoints import (
    batch_group_router,
    batch_job_router,
    batch_job_events_router,
    batch_job_event_details_router,
    common_router,
)

api_router = APIRouter()
api_router.include_router(
    router=batch_group_router, prefix="/batch-group", tags=["group"]
)
api_router.include_router(
    router=batch_job_router, prefix="/batch-job", tags=["job"]
)
api_router.include_router(
    router=batch_job_events_router, prefix="/batch-job-events", tags=["job-events"]
)
api_router.include_router(
    router=batch_job_event_details_router, prefix="/batch-job-event-details", tags=["job-event-details"]
)
# api_router.include_router(
#     router=common_router, prefix="", tags=["basic"]
# )
