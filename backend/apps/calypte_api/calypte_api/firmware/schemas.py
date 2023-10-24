from datetime import datetime
from uuid import UUID

from fastapi import Form, UploadFile
from pydantic import BaseModel, Field


class BaseFirmwareSchema(BaseModel):
    ...


class UploadFirmwareRequestBody:
    def __init__(
        self,
        firmware: UploadFile,
        name: str = Form(),
        version: str = Form(),
        description: str = Form(),
    ):
        self.firmware = firmware
        self.name = name
        self.version = version
        self.description = description


class FirmwareInfoResponse(BaseFirmwareSchema):
    id: UUID
    name: str
    version: str
    description: str

    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UploadFirmwareResponse(BaseFirmwareSchema):
    id: UUID
    name: str
    version: str
    description: str

    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class DownloadFirmwareResponse(BaseFirmwareSchema):
    id: UUID
    name: str
    version: str
    description: str

    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
