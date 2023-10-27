from datetime import datetime
from uuid import UUID

from fastapi_pagination import Params
from pydantic import BaseModel, ConfigDict, Field


class BaseDeviceRequestSchema(BaseModel):
    ...


class GetDeviceQueryParams(BaseDeviceRequestSchema, Params):
    name: str | None = Field(alias="name", default=None)
    # tags: list[UUID] | None = Field(alias="tags")


class CreateDeviceRequestBody(BaseDeviceRequestSchema):
    name: str
    tags: list[UUID]


class UpdateDeviceRequestBody(BaseDeviceRequestSchema):
    name: str
    tags: list[UUID]


class BaseDeviceResponseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class CreateDeviceResponse(BaseDeviceResponseSchema):
    id: UUID
    name: str
    tags: list[UUID]

    registered_at: datetime | None = Field(alias="registeredAt")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateDeviceResponse(BaseDeviceResponseSchema):
    id: UUID
    name: str
    tags: list[UUID]

    registered_at: datetime | None = Field(alias="registeredAt")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetDeviceResponse(BaseDeviceResponseSchema):
    id: UUID
    name: str
    tags: list[UUID]

    registered_at: datetime | None = Field(alias="registeredAt")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
