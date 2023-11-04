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
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: UUID
    company_id: UUID

    name: str
    description: str | None
    secret_key: UUID

    created_at: datetime
    updated_at: datetime


class CreateTypeResponse(BaseTypeResponseSchema):
    ...


class UpdateTypeResponse(BaseTypeResponseSchema):
    ...


class GetTypeResponse(BaseTypeResponseSchema):
    ...
