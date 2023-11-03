from datetime import datetime
from uuid import UUID

from fastapi_pagination import Params
from pydantic import BaseModel, ConfigDict, Field


class BaseDeviceRequestSchema(BaseModel):
    ...


class GetDeviceQueryParams(BaseDeviceRequestSchema, Params):
    name: str | None = Field(default=None)
    tags: str | None = Field(default=None)
    type_id: UUID | None = Field(default=None)
    current_firmware_id: UUID | None = Field(default=None)
    serial_number: str | None = Field(default=None)

    @property
    def tags_list(self) -> list[UUID] | None:
        if self.tags is None:
            return None

        return [UUID(tag_id.strip()) for tag_id in self.tags.split(",")]


class CreateDeviceRequestBody(BaseDeviceRequestSchema):
    name: str
    description: str | None = Field(default=None)
    company_id: UUID
    type_id: UUID
    serial_number: str
    tags: list[UUID] | None = Field(default=None)


class UpdateDeviceRequestBody(BaseDeviceRequestSchema):
    name: str
    description: str | None = Field(default=None)
    serial_number: str
    tags: list[UUID]


class BaseDeviceResponseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: UUID

    name: str
    description: str | None
    registered_at: datetime | None
    serial_number: str

    company_id: UUID
    type_id: UUID
    tags: list[UUID]
    current_firmware_id: UUID | None

    created_at: datetime
    updated_at: datetime


class CreateDeviceResponse(BaseDeviceResponseSchema):
    ...


class UpdateDeviceResponse(BaseDeviceResponseSchema):
    ...


class GetDeviceResponse(BaseDeviceResponseSchema):
    ...
