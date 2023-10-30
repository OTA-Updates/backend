from collections.abc import AsyncGenerator

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)


async_session: async_sessionmaker | None
engine: None | AsyncEngine = None
redis: None | Redis = None


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
