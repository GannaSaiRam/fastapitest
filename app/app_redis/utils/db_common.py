from typing import List
from sqlalchemy import text

from db import async_session


async def async_values_creation(seq_name, value) -> List[int]:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(text(
                f"SELECT NEXTVAL('{seq_name}') FROM generate_series(1, {value});"
            ))
            return [tuple_[0] for tuple_ in result.fetchall()]
