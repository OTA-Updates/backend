from uuid import UUID

from calypte_api.common.dependencies import JwtClaims, check_permission
from calypte_api.common.user_roles import UserRole
from calypte_api.tags import schemas as tags_schemas
from calypte_api.tags.service import TagServiceType

from fastapi import APIRouter, Depends
from fastapi_pagination import Page


router = APIRouter()


@router.post(
    path="/tags",
    response_model=tags_schemas.CreateTagResponse,
    summary="Create a tag",
    description="create a tag",
    response_description="The created tag",
    status_code=201,
)
async def create_tag(
    create_tag_request_body: tags_schemas.CreateTagRequestBody,
    tag_service: TagServiceType,
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),
) -> tags_schemas.CreateTagResponse:
    return await tag_service.create_tag(
        user_id=jwt_claims.user.id,
        request_body=create_tag_request_body,
    )


@router.get(
    path="/tags",
    response_model=Page[tags_schemas.GetTagResponse],
    summary="Get a tags page",
    description="get a tags page",
    response_description="The page of tags",
    status_code=200,
)
async def get_tags_page(
    tag_service: TagServiceType,
    query_params: tags_schemas.GetTagQueryParams = Depends(
        tags_schemas.GetTagQueryParams
    ),
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),
) -> Page[tags_schemas.GetTagResponse]:
    return await tag_service.get_tags(
        user_id=jwt_claims.user.id,
        query_params=query_params,
    )


@router.get(
    path="/tags/{tag_id:uuid}",
    response_model=tags_schemas.GetTagResponse,
    summary="Get a tag",
    description="get a tag",
    response_description="The tag",
    status_code=200,
)
async def get_tag(
    tag_id: UUID,
    tag_service: TagServiceType,
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),
) -> tags_schemas.GetTagResponse:
    return await tag_service.get_tag(
        user_id=jwt_claims.user.id,
        tag_id=tag_id,
    )


@router.put(
    path="/tags/{tag_id:uuid}",
    response_model=tags_schemas.UpdateTagResponse,
    summary="Update a tag",
    description="update a tag",
    response_description="The updated tag",
    status_code=200,
)
async def update_tag(
    tag_id: UUID,
    update_tag_request_body: tags_schemas.UpdateTagRequestBody,
    tag_service: TagServiceType,
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),
) -> tags_schemas.UpdateTagResponse:
    return await tag_service.update_tag(
        user_id=jwt_claims.user.id,
        tag_id=tag_id,
        request_body=update_tag_request_body,
    )


@router.delete(
    path="/tags/{tag_id:uuid}",
    response_model=None,
    summary="Delete a tag",
    description="delete a tag",
    response_description="The deleted tag",
    status_code=204,
)
async def delete_tag(
    tag_id: UUID,
    tag_service: TagServiceType,
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),
) -> None:
    await tag_service.delete_tag(
        user_id=jwt_claims.user.id,
        tag_id=tag_id,
    )
