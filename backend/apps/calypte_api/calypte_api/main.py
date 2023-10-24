from contextlib import asynccontextmanager

from calypte_api.common.settings import get_settings
from calypte_api.devices.api.v1.routers import router as devices_router
from calypte_api.firmware.api.v1.routers import router as firmware_router
from calypte_api.tags.api.v1.routers import router as tags_router

import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    lifespan=lifespan,
    title=settings.service_name,
    description=settings.service_description,
    docs_url="/docs",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    version="0.1.0",
)


app.include_router(devices_router, prefix="/api/v1")
app.include_router(firmware_router, prefix="/api/v1")
app.include_router(tags_router, prefix="/api/v1")

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
