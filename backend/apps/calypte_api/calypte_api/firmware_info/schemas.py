from datetime import datetime
from uuid import UUID

from fastapi_pagination import Params
from pydantic import BaseModel, ConfigDict, Field


class BaseFirmwareRequestSchema(BaseModel):
    ...


class FirmwareInfoUpdateRequestBody(BaseFirmwareRequestSchema):
    name: str
    version: str
    description: str
    serial_number: str


class CreateFirmwareInfoRequestBody(BaseFirmwareRequestSchema):
    type_id: UUID
    name: str
    version: str
    description: str
    serial_number: str


class GetFirmwareInfoQueryParams(BaseFirmwareRequestSchema, Params):
    type_id: UUID | None = Field(default=None)
    name: str | None = Field(default=None)
    version: str | None = Field(default=None)
    serial_number: str | None = Field(default=None)


class BaseFirmwareResponseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: UUID
    company_id: UUID
    type_id: UUID

    name: str
    version: str
    description: str
    serial_number: str

    created_at: datetime
    updated_at: datetime


class UpdateFirmwareInfoResponse(BaseFirmwareResponseSchema):
    ...


class CreateFirmwareInfoResponse(BaseFirmwareResponseSchema):
    ...


class GetFirmwareInfoResponse(BaseFirmwareResponseSchema):
    ...
