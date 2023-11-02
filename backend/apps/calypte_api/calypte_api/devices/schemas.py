from collections.abc import Sequence
from datetime import datetime
from uuid import UUID

from fastapi_pagination import Params
from pydantic import BaseModel, ConfigDict, Field


class BaseDeviceRequestSchema(BaseModel):
    ...


class GetDeviceQueryParams(BaseDeviceRequestSchema, Params):
    # TODO: figure out how to define a list in query params
    name: str | None = Field(default=None)
    tags: Sequence[UUID] | None = Field(alias="tags")
    type_id: UUID | None = Field(default=None)
    firmware_info_id: UUID | None = Field(default=None)


class CreateDeviceRequestBody(BaseDeviceRequestSchema):
    name: str
    description: str | None = Field(default=None)
    company_id: UUID
    type_id: UUID
    firmware_info_id: UUID | None
    tags: list[UUID]


class UpdateDeviceRequestBody(BaseDeviceRequestSchema):
    name: str
    description: str | None = Field(default=None)
    firmware_info_id: UUID | None
    tags: list[UUID]


class BaseDeviceResponseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class CreateDeviceResponse(BaseDeviceResponseSchema):
    id: UUID

    name: str
    description: str | None
    registered_at: datetime | None

    company_id: UUID
    type_id: UUID
    tags: list[UUID]
    firmware_info_id: UUID | None

    created_at: datetime
    updated_at: datetime


class UpdateDeviceResponse(BaseDeviceResponseSchema):
    id: UUID

    company_id: UUID
    name: str
    description: str | None
    registered_at: datetime | None

    type_id: UUID
    tags: list[UUID]
    firmware_info_id: UUID | None

    created_at: datetime
    updated_at: datetime


class GetDeviceResponse(BaseDeviceResponseSchema):
    id: UUID

    company_id: UUID
    name: str
    description: str | None
    registered_at: datetime | None

    type_id: UUID
    firmware_info_id: UUID
    tags: list[UUID]

    created_at: datetime
    updated_at: datetime
