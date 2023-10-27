from uuid import UUID

from calypte_api.common.dependencies import JwtClaims, check_permission
from calypte_api.common.user_roles import UserRole
from calypte_api.devices import schemas as device_schemas
from calypte_api.devices.service import DeviceServiceType

from fastapi import APIRouter, Depends
from fastapi_pagination import Page


router = APIRouter()


@router.post(
    path="/devices",
    response_model=device_schemas.CreateDeviceResponse,
    summary="Create a device",
    description="Create a device",
    response_description="The created device",
    status_code=201,
)
async def create_device(
    create_device_request_body: device_schemas.CreateDeviceRequestBody,
    device_service: DeviceServiceType,
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),
) -> device_schemas.CreateDeviceResponse:
    return await device_service.create_device(
        user_id=jwt_claims.user.id,
        request_body=create_device_request_body,
    )


@router.get(
    path="/devices",
    response_model=Page[device_schemas.GetDeviceResponse],
    summary="get paginated list of devices",
    description="get paginated list of devices",
    response_description="page of devices",
    status_code=200,
)
async def retrieve_devices(
    device_service: DeviceServiceType,
    query_params: device_schemas.GetDeviceQueryParams = Depends(
        device_schemas.GetDeviceQueryParams
    ),
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),
) -> Page[device_schemas.GetDeviceResponse]:
    return await device_service.get_devices(
        user_id=jwt_claims.user.id,
        query_params=query_params,
    )


@router.get(
    path="/devices/{device_id:uuid}",
    response_model=device_schemas.GetDeviceResponse,
    summary="get a device",
    description="get a device",
    response_description="the device",
    status_code=200,
)
async def retrieve_device(
    device_id: UUID,
    device_service: DeviceServiceType,
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),
) -> device_schemas.GetDeviceResponse:
    return await device_service.get_device(
        user_id=jwt_claims.user.id,
        device_id=device_id,
    )


@router.put(
    path="/devices/{device_id:uuid}",
    response_model=device_schemas.UpdateDeviceResponse,
    summary="update a device",
    description="update a device",
    response_description="the updated device",
    status_code=200,
)
async def update_device(
    device_id: UUID,
    update_device_request_body: device_schemas.UpdateDeviceRequestBody,
    device_service: DeviceServiceType,
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),
) -> device_schemas.UpdateDeviceResponse:
    return await device_service.update_device(
        user_id=jwt_claims.user.id,
        device_id=device_id,
        request_body=update_device_request_body,
    )


@router.delete(
    path="/devices/{device_id:uuid}",
    summary="delete a device",
    description="delete a device",
    response_description="the deleted device",
    status_code=204,
)
async def delete_device(
    device_id: UUID,
    device_service: DeviceServiceType,
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),
) -> None:
    await device_service.delete_device(
        user_id=jwt_claims.user.id,
        device_id=device_id,
    )
