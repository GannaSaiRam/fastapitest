import json
import time

from config import PREFIX
from db import redis
from utils.log_adapter import get_logger

log = get_logger(__name__)


async def update_record(data: dict):
    time_ns = time.time_ns()
    add = f"_{data['data']['id']}"
    await redis.set(f"{PREFIX}_{data['table_name']}{add}_{time_ns}", json.dumps(data))
