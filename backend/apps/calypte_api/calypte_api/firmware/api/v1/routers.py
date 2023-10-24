from typing import Annotated
from uuid import UUID

from calypte_api.firmware import schemas as firmware_schemas

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
    create_firmware_request_body: Annotated[
        firmware_schemas.UploadFirmwareRequestBody, Depends()
    ],
) -> firmware_schemas.UploadFirmwareResponse:
    ...


@router.get(
    path="/firmware/{firmware_id:uuid}",
    response_model=firmware_schemas.DownloadFirmwareResponse,
    summary="Download a firmware",
    description=" Downloads existing firmware by given id",
    response_description="the firmware",
    status_code=200,
)
async def download_firmware(
    firmware_id: UUID,
) -> firmware_schemas.DownloadFirmwareResponse:
    ...


@router.get(
    path="/firmware/{firmware_id:uuid}/info",
    response_model=firmware_schemas.FirmwareInfoResponse,
    summary="get an information about the firmware",
    description="get a firmware meta data",
    response_description="the firmware meta data",
    status_code=200,
)
async def retrieve_firmware_info(
    firmware_id: UUID,
) -> firmware_schemas.FirmwareInfoResponse:
    ...


@router.delete(
    path="/firmware/{firmware_id:uuid}",
    response_model=None,
    summary="delete a firmware",
    description="delete a firmware",
    response_description="the deleted firmware",
    status_code=204,
)
async def delete_firmware(firmware_id: UUID) -> None:
    ...
