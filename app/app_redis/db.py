import psycopg2
import redis

from contextlib import contextmanager

from aioredis import from_url
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, scoped_session

from config import DATABASE_URL, DATABASE_URL_ASYNC, DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME, \
    REDIS_HOST, REDIS_PORT
from utils.log_adapter import get_logger

log = get_logger(__name__)
engine = create_engine(DATABASE_URL)
engine_async = create_async_engine(DATABASE_URL_ASYNC, echo=True,
                                   pool_size=10, max_overflow=10, pool_timeout=600
                                   )
async_session = sessionmaker(
    bind=engine_async, expire_on_commit=False, class_=AsyncSession
)
redis_db = 0
redis_connection = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=redis_db)
redis = from_url(url=f"redis://{REDIS_HOST}:{REDIS_PORT}", decode_responses=True)

conn = psycopg2.connect(
    host=DB_SERVER,
    port=5432,
    user=DB_USERNAME,
    password=DB_PASSWORD,
    dbname=DB_NAME,
)
cursor = conn.cursor()


@contextmanager
def scoped_db_connection(auto_commit=True):
    threadsafe_db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))
    try:
        yield threadsafe_db_session()
        if auto_commit:
            threadsafe_db_session.commit()
    except Exception as _:
        threadsafe_db_session.rollback()
        raise
    finally:
        threadsafe_db_session.remove()


async def get_session() -> AsyncSession:
    db = async_sessionmaker(autocommit=False, autoflush=False, bind=engine_async)()
    try:
        yield db
    except HTTPException as _:
        raise  # Re-raise HTTPException to propagate it
    except Exception as e:
        log.info(f"Error while execution: {e}")
        raise e
    finally:
        await db.close()
