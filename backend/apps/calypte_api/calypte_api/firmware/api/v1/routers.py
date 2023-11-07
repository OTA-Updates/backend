from typing import Annotated
from uuid import UUID

from calypte_api.common.dependencies import (
    JwtClaims,
    RateLimiterType,
    check_permission,
)
from calypte_api.common.user_roles import UserRole
from calypte_api.firmware import schemas as firmware_schemas
from calypte_api.firmware.service import FirmwareServiceType

from fastapi import APIRouter, Depends
from fastapi_pagination import Page


router = APIRouter()


@router.post(
    path="/firmware",
    response_model=firmware_schemas.CreateFirmwareResponse,
    summary="Upload a firmware",
    description="Upload a firmware",
    response_description="An information of the uploaded firmware",
    status_code=201,
)
async def upload_firmware(
    _: RateLimiterType,
    create_firmware_request_body: Annotated[
        firmware_schemas.CreateFirmwareRequestBody, Depends()
    ],
    firmware_service: FirmwareServiceType,
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),
) -> firmware_schemas.CreateFirmwareResponse:
    return await firmware_service.create_firmware(
        company_id=jwt_claims.user.id,
        request_body=create_firmware_request_body,
    )


@router.get(
    path="/firmware/{firmware_id:uuid}",
    summary="Download a firmware",
    description=" Downloads existing firmware by given id",
    response_description="the firmware",
    status_code=200,
    response_class=firmware_schemas.DownloadFirmwareResponse,
)
async def download_firmware(
    _: RateLimiterType,
    firmware_id: UUID,
    firmware_service: FirmwareServiceType,
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),
) -> firmware_schemas.DownloadFirmwareResponse:
    return await firmware_service.get_firmware(
        company_id=jwt_claims.user.id,
        firmware_id=firmware_id,
    )


@router.get(
    path="/firmware/info",
    response_model=Page[firmware_schemas.GetFirmwareInfoResponse],
    summary="get firmware info list",
    description="get a firmware meta data",
    response_description="the firmware meta data",
    status_code=200,
)
async def retrieve_firmware_list(
    _: RateLimiterType,
    firmware_info_service: FirmwareServiceType,
    query_params: firmware_schemas.GetFirmwareInfoQueryParams = Depends(  # noqa B008
        firmware_schemas.GetFirmwareInfoQueryParams
    ),
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),  # noqa B008
) -> Page[firmware_schemas.GetFirmwareInfoResponse]:
    return await firmware_info_service.get_firmware_info_list(
        company_id=jwt_claims.user.id,
        query_params=query_params,
    )


@router.get(
    path="/firmware/{firmware_id:uuid}/info",
    response_model=firmware_schemas.GetFirmwareInfoResponse,
    summary="get an information about the firmware",
    description="get a firmware meta data",
    response_description="the firmware meta data",
    status_code=200,
)
async def retrieve_firmware_info(
    _: RateLimiterType,
    firmware_id: UUID,
    firmware_info_service: FirmwareServiceType,
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),  # noqa B008
) -> firmware_schemas.GetFirmwareInfoResponse:
    return await firmware_info_service.get_firmware_info(
        company_id=jwt_claims.user.id,
        firmware_id=firmware_id,
    )


@router.put(
    path="/firmware/{firmware_id:uuid}/info",
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
    firmware_info_service: FirmwareServiceType,
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),  # noqa B008
) -> firmware_schemas.UpdateFirmwareInfoResponse:
    return await firmware_info_service.update_firmware_info(
        company_id=jwt_claims.user.id,
        firmware_id=firmware_id,
        request_body=update_request_body,
    )
