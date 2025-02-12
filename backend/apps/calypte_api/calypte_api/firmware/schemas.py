from datetime import datetime
from uuid import UUID

from fastapi import Form, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, ConfigDict, Field


class BaseFirmwareRequestSchema(BaseModel):
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


class BaseFirmwareResponseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class UploadFirmwareResponse(BaseFirmwareResponseSchema):
    id: UUID
    name: str
    version: str
    description: str

    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class DownloadFirmwareResponse(StreamingResponse):
    ...
