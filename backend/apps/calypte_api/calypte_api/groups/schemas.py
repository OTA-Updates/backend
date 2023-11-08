from datetime import datetime
from typing import Optional
from uuid import UUID

from calypte_api.groups.models import Group

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, ConfigDict


class BaseGroupRequestSchema(BaseModel):
    ...


class GroupFilter(Filter):
    name__like: Optional[str] = None  # noqa: UP007
    order_by: Optional[list[str]] = None  # noqa: UP007

    class Constants(Filter.Constants):
        model = Group
        order_by_choices = ["name", "created_at", "updated_at"]


class CreateGroupRequestBody(BaseGroupRequestSchema):
    name: str
    type_id: UUID


class UpdateGroupRequestBody(BaseGroupRequestSchema):
    name: str


class BaseGroupResponseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: UUID

    name: str

    company_id: UUID
    type_id: UUID

    created_at: datetime
    updated_at: datetime


class CreateGroupResponse(BaseGroupResponseSchema):
    ...


class UpdateGroupResponse(BaseGroupResponseSchema):
    ...


class GetGroupResponse(BaseGroupResponseSchema):
    ...
