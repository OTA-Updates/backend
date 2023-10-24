from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class BaseDeviceSchema(BaseModel):
    ...


class CreateDeviceRequestBody(BaseDeviceSchema):
    name: str
    tags: list[UUID]


class UpdateDeviceRequestBody(BaseDeviceSchema):
    name: str
    tags: list[UUID]


class CreateDeviceResponse(BaseDeviceSchema):
    id: UUID
    name: str
    tags: list[UUID]

    registered_at: datetime = Field(alias="registeredAt")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateDeviceResponse(BaseDeviceSchema):
    id: UUID
    name: str
    tags: list[UUID]

    registered_at: datetime = Field(alias="registeredAt")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetDeviceResponse(BaseDeviceSchema):
    id: UUID
    name: str
    tags: list[UUID]

    registered_at: datetime = Field(alias="registeredAt")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
