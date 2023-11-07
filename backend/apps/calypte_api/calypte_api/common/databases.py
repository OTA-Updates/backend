from collections.abc import AsyncGenerator

from miniopy_async import Minio
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)


async_session: async_sessionmaker | None
engine: None | AsyncEngine = None
redis: None | Redis = None
minio_client: None | Minio = None


async def get_minio_client() -> Minio:
    if minio_client is None:
        raise RuntimeError("Minio client has not been defined.")

    return minio_client


async def get_db_session() -> AsyncGenerator[None, AsyncSession]:
    global async_session

    if async_session is None:
        raise RuntimeError("SQL client has not been defined.")

    async with async_session() as session:
        yield session


async def get_redis_client() -> Redis:
    if redis is None:
        raise RuntimeError("Redis client has not been defined.")

    return redis
