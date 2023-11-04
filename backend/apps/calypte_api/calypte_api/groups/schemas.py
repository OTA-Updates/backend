from datetime import datetime
from uuid import UUID

from fastapi_pagination import Params
from pydantic import BaseModel, ConfigDict, Field


class BaseGroupRequestSchema(BaseModel):
    ...


class GetGroupQueryParams(BaseGroupRequestSchema, Params):
    name: str | None = Field(default=None)
    type_id: UUID | None = Field(default=None)


class CreateGroupRequestBody(BaseGroupRequestSchema):
    name: str
    assigned_firmware_id: UUID | None
    type_id: UUID


class UpdateGroupRequestBody(BaseGroupRequestSchema):
    name: str
    assigned_firmware_id: UUID | None


class BaseGroupResponseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: UUID

    name: str

    company_id: UUID
    type_id: UUID
    assigned_firmware_id: UUID | None

    created_at: datetime
    updated_at: datetime


class CreateGroupResponse(BaseGroupResponseSchema):
    ...


class UpdateGroupResponse(BaseGroupResponseSchema):
    ...


class GetGroupResponse(BaseGroupResponseSchema):
    ...
