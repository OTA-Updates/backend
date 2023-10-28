from contextlib import asynccontextmanager

from calypte_api.common import databases
from calypte_api.common.settings import get_settings
from calypte_api.devices.api.v1.routers import router as devices_router
from calypte_api.firmware.api.v1.routers import router as firmware_router
from calypte_api.firmware_info.api.v1.routers import router as firmware_info_router
from calypte_api.tags.api.v1.routers import router as tags_router

import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_limiter import FastAPILimiter
from fastapi_pagination import add_pagination
from redis import asyncio as aioredis
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    databases.engine = create_async_engine(
        settings.postgres_dsn(), echo=settings.debug, future=True
    )
    databases.async_session = async_sessionmaker(
        databases.engine, expire_on_commit=False
    )
    databases.redis = aioredis.from_url(settings.redis_dsn(), encoding="utf-8")
    await FastAPILimiter.init(databases.redis)

    yield

    if databases.engine:
        await databases.engine.dispose()

    if databases.redis:
        await databases.redis.close()


app = FastAPI(
    lifespan=lifespan,
    title=settings.service_name,
    description=settings.service_description,
    docs_url="/docs",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    version="0.1.0",
)


app.include_router(devices_router, prefix="/api/v1", tags=["devices"])
app.include_router(firmware_router, prefix="/api/v1", tags=["firmware"])
app.include_router(tags_router, prefix="/api/v1", tags=["tags"])
app.include_router(firmware_info_router, prefix="/api/v1", tags=["firmware-info"])

add_pagination(app)


@app.get("/ping")
def pong() -> dict[str, str]:
    return {"ping": "pong!"}


if __name__ == "__main__":
    uvicorn.run(
        "calypte_api.main:app",
        host=settings.service_host,
        port=settings.service_port,
        reload=settings.debug,
    )
