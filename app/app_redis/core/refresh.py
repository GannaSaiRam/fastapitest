import copy
import json
import os
import re
import time
from collections import defaultdict
from json import JSONDecodeError

from config import PREFIX, TABLE_NAMES
from db import redis_connection, cursor, conn


upsert_query = """INSERT INTO {} ({})
VALUES ({})
ON CONFLICT(id)
DO UPDATE SET {};"""
insert_query = """WITH
cte AS (
    {values_with_col_name}
)
INSERT INTO {table_name} ({columns})
SELECT {is_distinct} {columns}
FROM cte;"""
update_query = """WITH cte AS (
    {values_with_col_name}
)
UPDATE {table_name} e
SET {columns}
FROM cte cte
WHERE e.id = cte.id
"""
not_null_restrictions = {
    TABLE_NAMES["TABLES"][0]: {
        "name": "",
    },
    TABLE_NAMES["TABLES"][1]: {
        "name": "",
        "processing_env": "",
    },
    TABLE_NAMES["TABLES"][2]: {
        "batch_job_id": 0,
        "event": ""
    },
    TABLE_NAMES["TABLES"][3]: {
        "batch_job_details_id": 0,
        "event": "",
    }
}
LIMIT = 100


def invalid_data(value: str) -> tuple:
    try:
        value = json.loads(value)
    except JSONDecodeError:
        return ()
    except Exception as e:
        print(f"Unknown exception: {e}")
        return ()
    table_name = value.get("table_name")
    if not table_name:
        return ()
    data = value.get("data")
    if not data:
        return ()
    type_in = value.get("type")
    if type_in not in ("insert", "update"):
        return ()
    field_types = value.get("field_types")
    if not field_types:
        return ()
    return table_name, data, type_in, field_types


def instance_mapping(v):
    if isinstance(v, str):
        return f"'{v}'"
    elif isinstance(v, type(None)):
        return 'null'
    return f'{v}'


def type_mapping(field_types, k):
    match field_types.get(k):
        case 'date':
            return "::date"
        case "datetime":
            return "::timestamp"
        case 'int':
            return "::bigint"
        case _:
            return ""


def push_to_pg(table_name: str):
    redis_keys: list[bytes] = redis_connection.keys(f"{PREFIX}_{table_name}*")
    count = 0
    for key in sorted(redis_keys, key=lambda d: int(str(d)[:-1].split('_')[-1])):
        count += 1
        copy_not_null_restrictions = copy.deepcopy(not_null_restrictions)
        try:
            value = json.loads(redis_connection.get(key))
        except JSONDecodeError:
            continue
        except Exception as e:
            print(f"Unknown exception: {e}")
            continue
        table_name = value.get("table_name")
        if not table_name:
            continue
        data = value.get("data")
        if not data:
            continue
        keys, values = [], []
        for k in data:
            keys.append(str(k))
            values.append(instance_mapping(data[k]))
            if k in copy_not_null_restrictions.get(table_name, {}):
                del copy_not_null_restrictions[table_name][k]
        extra_keys, extra_values = [], []
        for k in copy_not_null_restrictions.get(table_name, {}):
            extra_keys.append(str(k))
            extra_values.append(instance_mapping(copy_not_null_restrictions[table_name][k]))
        query = upsert_query.format(table_name, ", ".join(keys + extra_keys), ", ".join(values + extra_values),
                                    ", ".join([f"{k} = EXCLUDED.{k}" for k in keys]))
        print(query)
        cursor.execute(query)
        redis_connection.delete(key)
        if count >= LIMIT:
            conn.commit()
            count = 0
    # Commit the transaction
    if count > 0:
        conn.commit()
    os.environ[f'REFRESHING_{table_name}'] = 'true'


def parse_keys(table_name: str) -> dict[str, list]:
    redis_keys: list[bytes] = redis_connection.keys(f"{PREFIX}_{table_name}*")
    pattern = re.compile(fr'^{PREFIX}_{table_name}_(?P<id>[\dA-Z]+)_(?P<timestamp>\d+)$')
    grouped_records = defaultdict(list)
    for key in redis_keys:
        match = pattern.match(key.decode('utf-8'))
        if not match:
            continue
        record_id = match.group('id')
        timestamp = int(match.group('timestamp'))
        value = redis_connection.get(key).decode('utf-8')  # Assuming the value is a simple string; adjust if necessary
        grouped_records[record_id].append((timestamp, value, key))
        grouped_records[record_id].sort(key=lambda x: x[0])
    return grouped_records


def create_batches(grouped_records: dict[str, list], batch_size=LIMIT, all_insert=False):
    batches = []
    current_batch = []
    for records in grouped_records.values():
        if all_insert:
            current_batch.extend(records)
        else:
            current_batch.extend([records[0], records[-1]])
        if len(current_batch) >= batch_size:
            batches.append(current_batch)
            current_batch = []
    if current_batch:
        batches.append(current_batch)
    return batches


def upsert_batch(batch: list[tuple], table_name: str):
    redis_keys = []
    insert_values_with_col_name = defaultdict(list)
    update_values_with_col_name = defaultdict(list)
    for (_, value, key) in batch:
        if not (valid := invalid_data(value)):
            continue
        table_name, data, type_in, field_types = valid
        keys = list()
        for k in data:
            keys.append(str(k))
        if type_in == "insert":
            insert_values_with_col_name[tuple(sorted(keys))].append(
                f"""SELECT {', '.join(['{}{} as {}'.format(instance_mapping(v), type_mapping(field_types, k), k)
                                       for k, v in data.items()])}"""
            )
        elif type_in == "update":
            update_values_with_col_name[tuple(sorted(keys))].append(
                f"""SELECT {', '.join(['{}{} as {}'.format(instance_mapping(v), type_mapping(field_types, k), k)
                                       for k, v in data.items()])}"""
            )
        redis_keys.append(key)
    insert_query_with_values, update_query_with_values = "", ""
    cursor_batch = conn.cursor()
    try:
        commit = False
        cursor_batch.execute("BEGIN;")
        for key in insert_values_with_col_name:
            insert_query_with_values = insert_query.format(
                is_distinct=(
                    "distinct" if table_name != f'{TABLE_NAMES["SCHEMAS"][3]}.{TABLE_NAMES["TABLES"][3]}' else ""
                ),
                table_name=table_name,
                columns=", ".join(key),
                values_with_col_name="\nUNION ALL\n".join(insert_values_with_col_name[key])
            )
            cursor_batch.execute(insert_query_with_values)
            commit = True
        for key in update_values_with_col_name:
            update_query_with_values = update_query.format(
                table_name=table_name,
                columns=", ".join([f"{k} = cte.{k}" for k in key]),
                values_with_col_name="\nUNION ALL\n".join(update_values_with_col_name[key])
            )
            cursor_batch.execute(update_query_with_values)
            commit = True
        if commit:
            cursor_batch.execute("COMMIT;")
    except Exception as e:
        cursor_batch.execute("ROLLBACK;")
        print("insert:", insert_query_with_values, "update:", update_query_with_values)
        raise e
    finally:
        cursor_batch.close()
    return redis_keys


async def push_to_pg_batch(table_name: str):
    os.environ[f'REFRESHING_{table_name}'] = 'false'
    grouped_records: dict[str, list] = parse_keys(table_name=table_name)
    batches: list[list] = create_batches(
        grouped_records, all_insert=table_name == f'{TABLE_NAMES["SCHEMAS"][3]}.{TABLE_NAMES["TABLES"][3]}'
    )
    for batch in batches:
        try:
            keys = upsert_batch(batch=batch, table_name=table_name)
        except Exception as e:
            print(e)
            keys = []
        for key in keys:
            redis_connection.delete(key)
    if batches:
        print(time.time())
    os.environ[f'REFRESHING_{table_name}'] = 'true'
