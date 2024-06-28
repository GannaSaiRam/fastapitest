import json
import time

from config import PREFIX
from db import redis
from utils.log_adapter import get_logger

log = get_logger(__name__)


async def insert_record(data: dict, uniques=("id",)):
    time_ns = time.time_ns()
    add = "_"
    for i in uniques:
        add += f"{data['data'][i]}"
    await redis.set(f"{PREFIX}_{data['table_name']}{add}_{time_ns}", json.dumps(data))
