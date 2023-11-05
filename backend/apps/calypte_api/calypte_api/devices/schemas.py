from datetime import datetime
from uuid import UUID

from fastapi_pagination import Params
from pydantic import BaseModel, ConfigDict, Field


class BaseDeviceRequestSchema(BaseModel):
    ...


class GetDeviceQueryParams(BaseDeviceRequestSchema, Params):
    name: str | None = Field(default=None)
    group_id: UUID | None = Field(default=None)
    type_id: UUID | None = Field(default=None)
    current_firmware_id: UUID | None = Field(default=None)
    serial_number: str | None = Field(default=None)


class CreateDeviceRequestBody(BaseDeviceRequestSchema):
    name: str
    description: str | None
    assigned_firmware_id: UUID
    type_id: UUID
    serial_number: str
    group_id: UUID


class UpdateDeviceRequestBody(BaseDeviceRequestSchema):
    name: str
    description: str | None
    assigned_firmware_id: UUID
    serial_number: str
    group_id: UUID


class BaseDeviceResponseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: UUID

    name: str
    description: str | None
    registered_at: datetime | None
    serial_number: str

    company_id: UUID
    type_id: UUID
    group_id: UUID
    current_firmware_id: UUID | None
    assigned_firmware_id: UUID

    created_at: datetime
    updated_at: datetime


class CreateDeviceResponse(BaseDeviceResponseSchema):
    ...


class UpdateDeviceResponse(BaseDeviceResponseSchema):
    ...


class GetDeviceResponse(BaseDeviceResponseSchema):
    ...
