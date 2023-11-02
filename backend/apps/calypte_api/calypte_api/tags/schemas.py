from datetime import datetime
from uuid import UUID

from fastapi_pagination import Params
from pydantic import BaseModel, ConfigDict, Field


class BaseTagRequestSchema(BaseModel):
    ...


class GetTagQueryParams(BaseTagRequestSchema, Params):
    name: str | None = Field(default=None)


class CreateTagRequestBody(BaseTagRequestSchema):
    name: str

    type_id: UUID


class UpdateTagRequestBody(BaseTagRequestSchema):
    name: str


class BaseTagResponseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class CreateTagResponse(BaseTagResponseSchema):
    id: UUID
    name: str

    company_id: UUID
    type_id: UUID

    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateTagResponse(BaseTagResponseSchema):
    id: UUID
    name: str

    company_id: UUID
    type_id: UUID

    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetTagResponse(BaseTagResponseSchema):
    id: UUID
    name: str

    company_id: UUID
    type_id: UUID

    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
