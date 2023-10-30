from datetime import datetime
from uuid import UUID

from fastapi_pagination import Params
from pydantic import BaseModel, ConfigDict, Field


class BaseDeviceRequestSchema(BaseModel):
    ...


class GetDeviceQueryParams(BaseDeviceRequestSchema, Params):
    # TODO: figure out how to define a list in query params
    # tags: list[UUID] | None = Field(alias="tags")
    ...


class CreateDeviceRequestBody(BaseDeviceRequestSchema):
    type_id: UUID
    tags: list[UUID]


class UpdateDeviceRequestBody(BaseDeviceRequestSchema):
    tags: list[UUID]


class BaseDeviceResponseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class CreateDeviceResponse(BaseDeviceResponseSchema):
    id: UUID
    registered_at: datetime | None = Field(alias="registeredAt")

    type_id: UUID
    tags: list[UUID]
    firmware_info: list[UUID]

    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateDeviceResponse(BaseDeviceResponseSchema):
    id: UUID

    type_id: UUID
    tags: list[UUID]
    firmware_info: list[UUID]

    registered_at: datetime | None = Field(alias="registeredAt")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetDeviceResponse(BaseDeviceResponseSchema):
    id: UUID

    type_id: UUID
    tags: list[UUID]
    firmware_info: list[UUID]

    registered_at: datetime | None = Field(alias="registeredAt")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
