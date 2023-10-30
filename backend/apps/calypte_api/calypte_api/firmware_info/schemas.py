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


class CreateFirmwareInfoRequestBody(BaseFirmwareRequestSchema):
    type_id: UUID

    name: str
    version: str
    description: str


class GetFirmwareInfoQueryParams(BaseFirmwareRequestSchema, Params):
    type_id: UUID | None = Field(default=None)
    name: str | None = Field(default=None)
    device: str | None = Field(default=None)


class BaseFirmwareResponseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class UpdateFirmwareInfoResponse(BaseFirmwareResponseSchema):
    id: UUID
    type_id: UUID | None = Field(default=None)

    name: str
    version: str
    description: str

    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class CreateFirmwareInfoResponse(BaseFirmwareResponseSchema):
    id: UUID
    type_id: UUID | None = Field(default=None)

    name: str
    version: str
    description: str

    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetFirmwareInfoResponse(BaseFirmwareResponseSchema):
    id: UUID
    type_id: UUID | None = Field(default=None)

    name: str
    version: str
    description: str

    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
