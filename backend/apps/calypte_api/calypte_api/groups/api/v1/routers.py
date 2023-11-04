from uuid import UUID

from calypte_api.common.dependencies import (
    JwtClaims,
    RateLimiterType,
    check_permission,
)
from calypte_api.common.user_roles import UserRole
from calypte_api.groups import schemas as groups_schemas
from calypte_api.groups.service import GroupServiceType

from fastapi import APIRouter, Depends
from fastapi_pagination import Page


router = APIRouter()


@router.post(
    path="/groups",
    response_model=groups_schemas.CreateGroupResponse,
    summary="Create a group",
    description="create a group",
    response_description="The created group",
    status_code=201,
)
async def create_group(
    _: RateLimiterType,
    create_group_request_body: groups_schemas.CreateGroupRequestBody,
    group_service: GroupServiceType,
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),  # noqa B008
) -> groups_schemas.CreateGroupResponse:
    return await group_service.create_group(
        company_id=jwt_claims.user.id,
        request_body=create_group_request_body,
    )


@router.get(
    path="/groups",
    response_model=Page[groups_schemas.GetGroupResponse],
    summary="Get a groups page",
    description="get a groups page",
    response_description="The page of groups",
    status_code=200,
)
async def get_groups_page(
    _: RateLimiterType,
    group_service: GroupServiceType,
    query_params: groups_schemas.GetGroupQueryParams = Depends(  # noqa B008
        groups_schemas.GetGroupQueryParams
    ),
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),  # noqa B008
) -> Page[groups_schemas.GetGroupResponse]:
    return await group_service.get_groups(
        company_id=jwt_claims.user.id,
        query_params=query_params,
    )


@router.get(
    path="/groups/{group_id:uuid}",
    response_model=groups_schemas.GetGroupResponse,
    summary="Get a group",
    description="get a group",
    response_description="The group",
    status_code=200,
)
async def get_group(
    _: RateLimiterType,
    group_id: UUID,
    group_service: GroupServiceType,
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),  # noqa B008
) -> groups_schemas.GetGroupResponse:
    return await group_service.get_group(
        company_id=jwt_claims.user.id,
        group_id=group_id,
    )


@router.put(
    path="/groups/{group_id:uuid}",
    response_model=groups_schemas.UpdateGroupResponse,
    summary="Update a group",
    description="update a group",
    response_description="The updated group",
    status_code=200,
)
async def update_group(
    _: RateLimiterType,
    group_id: UUID,
    update_group_request_body: groups_schemas.UpdateGroupRequestBody,
    group_service: GroupServiceType,
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),  # noqa B008
) -> groups_schemas.UpdateGroupResponse:
    return await group_service.update_group(
        company_id=jwt_claims.user.id,
        group_id=group_id,
        request_body=update_group_request_body,
    )


@router.delete(
    path="/groups/{group_id:uuid}",
    response_model=None,
    summary="Delete a group",
    description="delete a group",
    response_description="The deleted group",
    status_code=204,
)
async def delete_group(
    _: RateLimiterType,
    group_id: UUID,
    group_service: GroupServiceType,
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),  # noqa B008
) -> None:
    await group_service.delete_group(
        company_id=jwt_claims.user.id,
        group_id=group_id,
    )
