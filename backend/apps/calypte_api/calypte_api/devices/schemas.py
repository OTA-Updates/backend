from datetime import datetime
from typing import Optional
from uuid import UUID

from calypte_api.devices.models import Device

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, ConfigDict


class BaseDeviceRequestSchema(BaseModel):
    ...


class DeviceFilter(Filter):
    name__like: Optional[str] = None  # noqa: UP007
    type_id: Optional[UUID] = None  # noqa: UP007
    group_id: Optional[str] = None  # noqa: UP007
    current_firmware_id: Optional[str] = None  # noqa: UP007
    serial_number__like: Optional[str] = None  # noqa: UP007
    order_by: Optional[list[str]] = None  # noqa: UP007

    class Constants(Filter.Constants):
        model = Device
        order_by_choices = ["name", "created_at", "updated_at"]


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
