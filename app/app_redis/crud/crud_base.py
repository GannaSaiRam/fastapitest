import json
from datetime import datetime
from typing import Dict, Any, List
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import Sequence, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.background import BackgroundTasks

from config import PREFIX
from core import insert_record, update_record, delete_record
from db import redis_connection
from post_request_bodies import SequenceFormatBody
from schemas.base import BaseSchema
from utils.common import extract_type
from utils.db_common import async_values_creation
from utils.log_adapter import get_logger

log = get_logger(__name__)


class CRUDBase:
    def __init__(self, model, sequence):
        self.model = model
        self.sequence: Sequence = sequence

    @staticmethod
    def truncate_list(main_list, lengths):
        result = []
        current_index = 0
        for length in lengths:
            sublist = main_list[current_index:current_index + length]
            result.append(sublist)
            current_index += length
        return result

    async def get_next_sequence_value(
            self,
            *,
            sequence_dict: SequenceFormatBody = None
    ):
        if sequence_dict is None:
            sequence_dict = 1
        else:
            sequence_dict = sequence_dict.sequence_dict
        if isinstance(sequence_dict, Dict):
            all_values = [v for v in sequence_dict.values()]
            total = sum(all_values)
            total_seqs = await async_values_creation(self.sequence.name, total)
            truncates_lists = self.truncate_list(total_seqs, all_values)
            returning_map_with_seqs: Dict[Any, List[int]] = {
                key: result for key, result in zip(sequence_dict.keys(), truncates_lists)}
            return returning_map_with_seqs
        elif isinstance(sequence_dict, List):
            all_values = [v for v in sequence_dict]
            total = sum(all_values)
            total_seqs = await async_values_creation(self.sequence.name, total)
            truncates_lists = self.truncate_list(total_seqs, all_values)
            returning_list_with_seqs: List[List[int]] = truncates_lists
            return returning_list_with_seqs
        returning_int_with_seqs = await async_values_creation(self.sequence.name, sequence_dict)
        return returning_int_with_seqs

    def create(self, *, data: BaseModel, field_types: dict, uniques=("id",), background_tasks: BackgroundTasks):
        log.info(f'Create: {data} for table: {self.model.schema_name()}.{self.model.table_name()}')
        data = jsonable_encoder(data)
        field_types = {k: str(extract_type(v)) for k, v in field_types.items()}
        background_tasks.add_task(
            insert_record, {
                "data": data,
                "table_name": f"{self.model.schema_name()}.{self.model.table_name()}",
                "type": "insert",
                "field_types": field_types,
            }, uniques=uniques,
        )

    async def get_by_id_rs(self, *, _id: int) -> dict:
        redis_keys: list[bytes] = redis_connection.keys(f"{PREFIX}_{self.model.table_name()}_{_id}_*")
        if redis_keys:
            redis_keys: list[str] = sorted([r.decode('utf-8') for r in redis_keys], key=lambda x: int(x.split("_")[-1]))
            value = json.loads(redis_connection.get(redis_keys[0]).decode('utf-8')).get("data", {})
            value.update(json.loads(redis_connection.get(redis_keys[-1]).decode('utf-8')).get("data", {}))
            return value
        return {}

    async def get_by_id_pg(self, *, _id: int, async_session: AsyncSession):
        log.info(f'Get by id: {_id} for table: {self.model.table_name()}')
        try:
            statement = select(self.model).filter(self.model.id == _id)
            result = await async_session.execute(statement)
            return result.scalars().one()
        except NoResultFound:
            return

    def update_status(
            self, *, _id: int, data: BaseModel, status: str, field_types: dict,
            background_tasks: BackgroundTasks
    ):
        log.info(f'Update status to: {status} by id: {_id} for table: {self.model.table_name()}')
        field_types = {k: str(extract_type(v)) for k, v in field_types.items()}
        data = jsonable_encoder(data)
        data["id"] = _id
        background_tasks.add_task(
            update_record, {
                "data": data,
                "table_name": f"{self.model.schema_name()}.{self.model.table_name()}",
                "type": "update",
                "field_types": field_types,
             },
        )

    def delete(self, *, data: BaseSchema, background_tasks: BackgroundTasks):
        log.info(f'Delete by id: {data.id} for table: {self.model.table_name()}')
        background_tasks.add_task(delete_record)
