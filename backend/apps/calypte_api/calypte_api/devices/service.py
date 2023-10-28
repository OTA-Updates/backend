from abc import ABC, abstractmethod
from typing import Annotated
from uuid import UUID

from calypte_api.devices.repository import DeviceRepositoryType, IDeviceRepo
from calypte_api.devices.schemas import (
    CreateDeviceRequestBody,
    CreateDeviceResponse,
    GetDeviceQueryParams,
    GetDeviceResponse,
    UpdateDeviceRequestBody,
    UpdateDeviceResponse,
)

from fastapi import Depends
from fastapi_pagination import Page


class IDeviceService(ABC):
    @abstractmethod
    async def get_device(
        self,
        user_id: UUID,
        device_id: UUID,
    ) -> GetDeviceResponse:
        """
        Get device by id

        Args:
            user_id (UUID): user id
            device_id (UUID): device id

        """

    @abstractmethod
    async def get_devices(
        self, user_id: UUID, query_params: GetDeviceQueryParams
    ) -> Page[GetDeviceResponse]:
        """
        Get all devices

        Args:
            user_id (UUID): user id

        """

    @abstractmethod
    async def create_device(
        self, user_id: UUID, request_body: CreateDeviceRequestBody
    ) -> CreateDeviceResponse:
        """
        Create device

        Args:
            user_id (UUID): user id
            request_body (CreateDeviceRequestBody): request body

        """

    @abstractmethod
    async def update_device(
        self,
        user_id: UUID,
        device_id: UUID,
        request_body: UpdateDeviceRequestBody,
    ) -> UpdateDeviceResponse:
        """
        Update device

        Args:
            user_id (UUID): user id
            device_id (UUID): device id
            request_body (CreateDeviceRequestBody): request body
        """

    @abstractmethod
    async def delete_device(self, user_id: UUID, device_id: UUID) -> None:
        """
        Delete device

        Args:
            user_id (UUID): user id
            device_id (UUID): device id
        """


class DeviceService(IDeviceService):
    def __init__(self, device_repo: IDeviceRepo):
        self.device_repo = device_repo

    async def get_device(
        self,
        user_id: UUID,
        device_id: UUID,
    ) -> GetDeviceResponse:
        return await self.device_repo.get_device_by_id(
            user_id=user_id, device_id=device_id
        )

    async def get_devices(
        self, user_id: UUID, query_params: GetDeviceQueryParams
    ) -> Page[GetDeviceResponse]:
        devices = await self.device_repo.get_devices(
            user_id=user_id, query_params=query_params
        )
        return Page.create(
            items=devices,
            params=query_params,
            total=query_params.size,
        )

    async def create_device(
        self, user_id: UUID, request_body: CreateDeviceRequestBody
    ) -> CreateDeviceResponse:
        return await self.device_repo.create_device(
            user_id=user_id,
            name=request_body.name,
            tags=request_body.tags,
        )

    async def update_device(
        self,
        user_id: UUID,
        device_id: UUID,
        request_body: UpdateDeviceRequestBody,
    ) -> UpdateDeviceResponse:
        return await self.device_repo.update_device(
            user_id=user_id,
            device_id=device_id,
            name=request_body.name,
            tags=request_body.tags,
        )

    async def delete_device(self, user_id: UUID, device_id: UUID) -> None:
        return await self.device_repo.delete_device(
            user_id=user_id, device_id=device_id
        )


def get_device_service(device_repo: DeviceRepositoryType) -> IDeviceService:
    return DeviceService(device_repo=device_repo)


DeviceServiceType = Annotated[IDeviceService, Depends(get_device_service)]
