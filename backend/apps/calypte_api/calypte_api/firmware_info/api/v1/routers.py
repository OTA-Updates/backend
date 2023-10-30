from uuid import UUID

from calypte_api.common.dependencies import JwtClaims, RateLimiterType, check_permission
from calypte_api.common.user_roles import UserRole
from calypte_api.firmware_info import schemas as firmware_schemas
from calypte_api.firmware_info.service import FirmwareInfoServiceType

from fastapi import APIRouter, Depends
from fastapi_pagination import Page


router = APIRouter()


@router.get(
    path="/firmware-info/",
    response_model=Page[firmware_schemas.GetFirmwareInfoResponse],
    summary="get firmware info list",
    description="get a firmware meta data",
    response_description="the firmware meta data",
    status_code=200,
)
async def retrieve_firmware_list(
    _: RateLimiterType,
    firmware_info_service: FirmwareInfoServiceType,
    query_params: firmware_schemas.GetFirmwareInfoQueryParams = Depends(
        firmware_schemas.GetFirmwareInfoQueryParams
    ),
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),
) -> Page[firmware_schemas.GetFirmwareInfoResponse]:
    return await firmware_info_service.get_firmware_list(
        user_id=jwt_claims.user.id,
        query_params=query_params,
    )


@router.get(
    path="/firmware-info/{firmware_id:uuid}",
    response_model=firmware_schemas.GetFirmwareInfoResponse,
    summary="get an information about the firmware",
    description="get a firmware meta data",
    response_description="the firmware meta data",
    status_code=200,
)
async def retrieve_firmware_info(
    _: RateLimiterType,
    firmware_id: UUID,
    firmware_info_service: FirmwareInfoServiceType,
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),
) -> firmware_schemas.GetFirmwareInfoResponse:
    return await firmware_info_service.get_firmware_info(
        user_id=jwt_claims.user.id,
        firmware_id=firmware_id,
    )


@router.put(
    path="/firmware-info/{firmware_id:uuid}",
    response_model=firmware_schemas.GetFirmwareInfoResponse,
    summary="get an information about the firmware",
    description="get a firmware meta data",
    response_description="the firmware meta data",
    status_code=200,
)
async def update_firmware_info(
    _: RateLimiterType,
    firmware_id: UUID,
    update_request_body: firmware_schemas.FirmwareInfoUpdateRequestBody,
    firmware_info_service: FirmwareInfoServiceType,
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),
) -> firmware_schemas.GetFirmwareInfoResponse:
    return await firmware_info_service.update_firmware(
        user_id=jwt_claims.user.id,
        firmware_id=firmware_id,
        request_body=update_request_body,
    )
