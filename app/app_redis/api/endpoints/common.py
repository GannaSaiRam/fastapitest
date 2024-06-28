import os
from asyncio import sleep as asyncio_sleep
from fastapi import APIRouter
from starlette.background import BackgroundTasks

from config import TABLE_NAMES
from core.refresh import push_to_pg_batch

router = APIRouter()


@router.post("/refresh", response_model=dict)
async def refresh_data(
        *,
        background_tasks: BackgroundTasks,
):
    returning = {}
    for tab_name in TABLE_NAMES["TABLES"]:
        if os.environ.get(f'REFRESHING_{tab_name}') == 'false':
            returning[tab_name] = "Skipping as there is existing refresh going"
        else:
            os.environ[f'REFRESHING_{tab_name}'] = 'false'
            background_tasks.add_task(push_to_pg_batch, *(tab_name,))
            returning[tab_name] = "Raised for refreshing"
    return returning


async def refreshing_data():
    if os.environ.get('REFRESHING') == 'true':
        os.environ['REFRESHING'] = 'true'
        return
    print("Initializing refresh")
    os.environ['REFRESHING'] = 'true'
    while True:
        for schema, tab_name in zip(TABLE_NAMES["SCHEMAS"], TABLE_NAMES["TABLES"]):
            if os.environ.get(f'REFRESHING_{schema}.{tab_name}') != 'false':
                await push_to_pg_batch(f'{schema}.{tab_name}',)
        await asyncio_sleep(15)
