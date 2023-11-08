from datetime import datetime
from typing import Optional
from uuid import UUID

from calypte_api.types.models import Type

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, ConfigDict


class BaseTypeRequestSchema(BaseModel):
    ...


class TypeFilter(Filter):
    name__like: Optional[str] = None  # noqa: UP007
    order_by: Optional[list[str]] = None  # noqa: UP007

    class Constants(Filter.Constants):
        model = Type
        order_by_choices = ["name", "created_at", "updated_at"]


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
