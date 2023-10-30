import asyncio

from collections.abc import AsyncGenerator

import pytest_asyncio

from calypte_api.common.databases import get_db_session
from calypte_api.common.models import BaseModel
from calypte_api.common.settings import get_settings
from calypte_api.main import app
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.schema import CreateSchema


settings = get_settings()


@pytest_asyncio.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def postgres_engine():
    engine = create_async_engine(
        settings.postgres_dsn(),
        echo=True,
    )

    async with engine.begin() as conn:
        await conn.execute(
            CreateSchema(
                settings.postgres_schema,
                if_not_exists=True,
            ),
        )
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def db_session(postgres_engine: AsyncEngine):
    async_session = async_sessionmaker(postgres_engine, expire_on_commit=False)

    async def override_get_db_session() -> AsyncGenerator[None, AsyncSession]:
        async with async_session() as db:
            yield db

    app.dependency_overrides[get_db_session] = override_get_db_session

    async with async_session() as db:
        yield db
