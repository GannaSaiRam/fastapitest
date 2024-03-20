import uvicorn
from fastapi import FastAPI
from mangum import Mangum

from app.api.api import api_router
from app.config import PORT


app = FastAPI(
    title='Batch Logging', openapi_url=f"/api/openapi.json"
)
app.include_router(api_router, prefix='')
handler = Mangum(app)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
