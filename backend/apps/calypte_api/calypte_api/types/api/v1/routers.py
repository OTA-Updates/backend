from uuid import UUID

from calypte_api.common.dependencies import (
    JwtClaims,
    RateLimiterType,
    check_permission,
)
from calypte_api.common.user_roles import UserRole
from calypte_api.types import schemas as type_schemas
from calypte_api.types.service import TypeServiceType

from fastapi import APIRouter, Depends
from fastapi_pagination import Page


router = APIRouter()


@router.post(
    path="/types",
    response_model=type_schemas.CreateTypeResponse,
    summary="Create a type",
    description="Create a type",
    response_description="The created type",
    status_code=201,
)
async def create_type(
    _: RateLimiterType,
    create_type_request_body: type_schemas.CreateTypeRequestBody,
    type_service: TypeServiceType,
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),  # noqa B008
) -> type_schemas.CreateTypeResponse:
    return await type_service.create_type(
        company_id=jwt_claims.user.id,
        request_body=create_type_request_body,
    )


@router.get(
    path="/types",
    response_model=Page[type_schemas.GetTypeResponse],
    summary="get paginated list of types",
    description="get paginated list of types",
    response_description="page of types",
    status_code=200,
)
async def retrieve_types(
    _: RateLimiterType,
    type_service: TypeServiceType,
    query_params: type_schemas.GetTypeQueryParams = Depends(  # noqa B008
        type_schemas.GetTypeQueryParams
    ),
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),  # noqa B008
) -> Page[type_schemas.GetTypeResponse]:
    return await type_service.get_types(
        company_id=jwt_claims.user.id,
        query_params=query_params,
    )


@router.get(
    path="/types/{type_id:uuid}",
    response_model=type_schemas.GetTypeResponse,
    summary="get a type",
    description="get a type",
    response_description="the type",
    status_code=200,
)
async def retrieve_type(
    _: RateLimiterType,
    type_id: UUID,
    type_service: TypeServiceType,
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),  # noqa B008
) -> type_schemas.GetTypeResponse:
    return await type_service.get_type(
        company_id=jwt_claims.user.id,
        type_id=type_id,
    )


@router.put(
    path="/types/{type_id:uuid}",
    response_model=type_schemas.UpdateTypeResponse,
    summary="update a type",
    description="update a type",
    response_description="the updated type",
    status_code=200,
)
async def update_type(
    _: RateLimiterType,
    type_id: UUID,
    update_type_request_body: type_schemas.UpdateTypeRequestBody,
    type_service: TypeServiceType,
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),  # noqa B008
) -> type_schemas.UpdateTypeResponse:
    return await type_service.update_type(
        company_id=jwt_claims.user.id,
        type_id=type_id,
        request_body=update_type_request_body,
    )


@router.delete(
    path="/types/{type_id:uuid}",
    summary="delete a type",
    description="delete a type",
    response_description="the deleted type",
    status_code=204,
)
async def delete_type(
    _: RateLimiterType,
    type_id: UUID,
    type_service: TypeServiceType,
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),  # noqa B008
) -> None:
    await type_service.delete_type(
        company_id=jwt_claims.user.id,
        type_id=type_id,
    )
