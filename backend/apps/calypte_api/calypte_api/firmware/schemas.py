from datetime import datetime
from typing import Optional
from uuid import UUID

from calypte_api.firmware.models import FirmwareInfo

from fastapi import Form, UploadFile
from fastapi.responses import StreamingResponse
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, ConfigDict


class BaseFirmwareRequestSchema(BaseModel):
    ...


class FirmwareInfoUpdateRequestBody(BaseFirmwareRequestSchema):
    name: str
    version: str
    description: str
    serial_number: str


class CreateFirmwareRequestBody:
    def __init__(
        self,
        firmware: UploadFile,
        name: str = Form(),
        version: str = Form(),
        description: str = Form(),
        serial_number: str = Form(),
        type_id: UUID = Form(),
    ):
        self.firmware = firmware
        self.name = name
        self.version = version
        self.description = description
        self.serial_number = serial_number
        self.type_id = type_id


class FirmwareFilter(Filter):
    name__like: Optional[str] = None  # noqa: UP007
    type_id: Optional[UUID] = None  # noqa: UP007
    version__like: Optional[str] = None  # noqa: UP007
    serial_number__like: Optional[str] = None  # noqa: UP007
    order_by: Optional[list[str]] = None  # noqa: UP007

    class Constants(Filter.Constants):
        model = FirmwareInfo
        order_by_choices = ["name", "created_at", "updated_at"]


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


class GetFirmwareInfoResponse(BaseFirmwareResponseSchema):
    ...


class CreateFirmwareResponse(BaseFirmwareResponseSchema):
    ...


class DownloadFirmwareResponse(StreamingResponse):
    ...
