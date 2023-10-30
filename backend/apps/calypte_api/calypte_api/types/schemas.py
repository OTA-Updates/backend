from datetime import datetime
from uuid import UUID

from fastapi_pagination import Params
from pydantic import BaseModel, ConfigDict, Field


class BaseTypeRequestSchema(BaseModel):
    ...


class GetTypeQueryParams(BaseTypeRequestSchema, Params):
    name: str | None = Field(alias="name", default=None)


class CreateTypeRequestBody(BaseTypeRequestSchema):
    name: str
    description: str | None


class UpdateTypeRequestBody(BaseTypeRequestSchema):
    name: str
    description: str | None


class BaseTypeResponseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class CreateTypeResponse(BaseTypeResponseSchema):
    id: UUID
    name: str
    description: str | None

    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class UpdateTypeResponse(BaseTypeResponseSchema):
    id: UUID
    name: str
    description: str | None

    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetTypeResponse(BaseTypeResponseSchema):
    id: UUID
    name: str
    description: str | None

    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
