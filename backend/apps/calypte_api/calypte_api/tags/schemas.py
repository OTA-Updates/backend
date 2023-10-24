from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class BaseTagSchema(BaseModel):
    ...


class CreateTagRequestBody(BaseTagSchema):
    name: str


class UpdateTagRequestBody(BaseTagSchema):
    name: str


class CreateTagResponse(BaseTagSchema):
    id: UUID
    name: str

    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateTagResponse(BaseTagSchema):
    id: UUID
    name: str

    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetTagResponse(BaseTagSchema):
    id: UUID
    name: str

    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
