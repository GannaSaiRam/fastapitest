import uvicorn

from asyncio import gather as asyncio_gather, run as asyncio_run
from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from api.api import api_router
from api.endpoints.common import refreshing_data
from config import PORT, logging_config

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.include_router(api_router, prefix='')


async def run_uvicorn():
    config = uvicorn.Config(app=app, host="0.0.0.0", port=PORT
                            # , log_config=logging_config
                            )
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    await asyncio_gather(
        run_uvicorn(),
        refreshing_data(),
    )

if __name__ == "__main__":
    asyncio_run(main())
