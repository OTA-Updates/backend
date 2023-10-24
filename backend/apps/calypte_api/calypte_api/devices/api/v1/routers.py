from uuid import UUID

from calypte_api.devices import schemas as device_schemas

from fastapi import APIRouter
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
) -> device_schemas.CreateDeviceResponse:
    ...


@router.get(
    path="/devices",
    response_model=Page[device_schemas.GetDeviceResponse],
    summary="get paginated list of devices",
    description="get paginated list of devices",
    response_description="page of devices",
    status_code=200,
)
async def retrieve_devices() -> Page[device_schemas.GetDeviceResponse]:
    ...


@router.get(
    path="/devices/{device_id:uuid}",
    response_model=device_schemas.GetDeviceResponse,
    summary="get a device",
    description="get a device",
    response_description="the device",
    status_code=200,
)
async def retrieve_device(device_id: UUID) -> device_schemas.GetDeviceResponse:
    ...


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
) -> device_schemas.UpdateDeviceResponse:
    ...


@router.delete(
    path="/devices/{device_id:uuid}",
    summary="delete a device",
    description="delete a device",
    response_description="the deleted device",
    status_code=204,
)
async def delete_device(device_id: UUID) -> None:
    ...
