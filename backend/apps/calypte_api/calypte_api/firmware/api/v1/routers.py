from typing import Annotated
from uuid import UUID

from calypte_api.common.dependencies import JwtClaims, RateLimiterType, check_permission
from calypte_api.common.user_roles import UserRole
from calypte_api.firmware import schemas as firmware_schemas
from calypte_api.firmware.serivce import FirmwareServiceType
from calypte_api.firmware_info import schemas as firmware_info_schemas
from calypte_api.firmware_info.service import FirmwareInfoServiceType

from fastapi import APIRouter, Depends


router = APIRouter()


@router.post(
    path="/firmware",
    response_model=firmware_schemas.UploadFirmwareResponse,
    summary="Upload a firmware",
    description="Upload a firmware",
    response_description="An information of the uploaded firmware",
    status_code=201,
)
async def upload_firmware(
    _: RateLimiterType,
    create_firmware_request_body: Annotated[
        firmware_schemas.UploadFirmwareRequestBody, Depends()
    ],
    firmware_info_service: FirmwareInfoServiceType,
    firmware_service: FirmwareServiceType,
    jwt_claims: JwtClaims = Depends(check_permission(UserRole.USER)),
) -> firmware_schemas.UploadFirmwareResponse:
    # TODO: combine these two calls into one transaction
    firmware_info = await firmware_info_service.create_firmware(
        user_id=jwt_claims.user.id,
        request_body=firmware_info_schemas.CreateFirmwareInfoRequestBody(
            name=create_firmware_request_body.name,
            version=create_firmware_request_body.version,
            description=create_firmware_request_body.description,
        ),
    )

    await firmware_service.upload_firmware(
        user_id=jwt_claims.user.id,
        firmware_id=firmware_info.id,
        firmware=create_firmware_request_body.firmware.file,
    )

    return firmware_info


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
    return await firmware_service.get_firmware_by_id(
        user_id=jwt_claims.user.id,
        firmware_id=firmware_id,
    )
