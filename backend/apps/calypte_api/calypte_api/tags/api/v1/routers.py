from uuid import UUID

from calypte_api.tags import schemas as tags_schemas

from fastapi import APIRouter
from fastapi_pagination import Page


router = APIRouter()


@router.post(
    path="/tags",
    response_model=tags_schemas.CreateTagRequestBody,
    summary="Create a tag",
    description="create a tag",
    response_description="The created tag",
    status_code=201,
)
async def create_tag(
    create_tag_request_body: tags_schemas.CreateTagRequestBody
) -> tags_schemas.CreateTagResponse:
    ...


@router.get(
    path="/tags",
    response_model=Page[tags_schemas.GetTagResponse],
    summary="Get a tags page",
    description="get a tags page",
    response_description="The page of tags",
    status_code=200,
)
async def get_tags_page() -> Page[tags_schemas.GetTagResponse]:
    ...


@router.get(
    path="/tags/{tag_id:uuid}",
    response_model=tags_schemas.GetTagResponse,
    summary="Get a tag",
    description="get a tag",
    response_description="The tag",
    status_code=200,
)
async def get_tag(tag_id: UUID) -> tags_schemas.GetTagResponse:
    ...


@router.put(
    path="/tags/{tag_id:uuid}",
    response_model=tags_schemas.UpdateTagRequestBody,
    summary="Update a tag",
    description="update a tag",
    response_description="The updated tag",
    status_code=200,
)
async def update_tag(
    tag_id: UUID, update_tag_request_body: tags_schemas.UpdateTagRequestBody
) -> tags_schemas.UpdateTagResponse:
    ...


@router.delete(
    path="/tags/{tag_id:uuid}",
    response_model=None,
    summary="Delete a tag",
    description="delete a tag",
    response_description="The deleted tag",
    status_code=204,
)
async def delete_tag(tag_id: UUID) -> None:
    ...
