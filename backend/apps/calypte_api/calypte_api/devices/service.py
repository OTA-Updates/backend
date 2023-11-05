from abc import ABC, abstractmethod
from typing import Annotated
from uuid import UUID

from calypte_api.common.exceptions import (
    DatabaseError,
    ObjectNotFoundError,
    RepositoryError,
)
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
        self, company_id: UUID, device_id: UUID
    ) -> GetDeviceResponse:
        """
        Get device by id

        Args:
            company_id (UUID): user id
            device_id (UUID): device id

        """

    @abstractmethod
    async def get_devices(
        self, company_id: UUID, query_params: GetDeviceQueryParams
    ) -> Page[GetDeviceResponse]:
        """
        Get all devices

        Args:
            company_id (UUID): user id

        """

    @abstractmethod
    async def create_device(
        self, company_id: UUID, request_body: CreateDeviceRequestBody
    ) -> CreateDeviceResponse:
        """
        Create device

        Args:
            company_id (UUID): user id
            request_body (CreateDeviceRequestBody): request body

        """

    @abstractmethod
    async def update_device(
        self,
        company_id: UUID,
        device_id: UUID,
        request_body: UpdateDeviceRequestBody,
    ) -> UpdateDeviceResponse:
        """
        Update device

        Args:
            company_id (UUID): user id
            device_id (UUID): device id
            request_body (CreateDeviceRequestBody): request body
        """

    @abstractmethod
    async def delete_device(self, company_id: UUID, device_id: UUID) -> None:
        """
        Delete device

        Args:
            company_id (UUID): user id
            device_id (UUID): device id
        """


class DeviceService(IDeviceService):
    def __init__(self, device_repo: IDeviceRepo):
        self.device_repo = device_repo

    async def get_device(
        self,
        company_id: UUID,
        device_id: UUID,
    ) -> GetDeviceResponse:
        device_schema = await self.device_repo.get_device_by_id(
            company_id=company_id, device_id=device_id
        )

        if device_schema is None:
            raise ObjectNotFoundError(object_id=device_id)

        return device_schema

    async def get_devices(
        self, company_id: UUID, query_params: GetDeviceQueryParams
    ) -> Page[GetDeviceResponse]:
        limit = query_params.size
        offset = (query_params.page - 1) * query_params.size

        devices = await self.device_repo.get_devices(
            company_id=company_id,
            limit=limit,
            offset=offset,
            group_id=query_params.group_id,
            serial_number=query_params.serial_number,
            current_firmware_id=query_params.current_firmware_id,
            type_id=query_params.type_id,
            name=query_params.name,
        )
        return Page.create(
            items=devices,
            params=query_params,
            total=query_params.size,
        )

    async def create_device(
        self, company_id: UUID, request_body: CreateDeviceRequestBody
    ) -> CreateDeviceResponse:
        try:
            return await self.device_repo.create_device(
                type_id=request_body.type_id,
                company_id=company_id,
                assigned_firmware_id=request_body.assigned_firmware_id,
                serial_number=request_body.serial_number,
                name=request_body.name,
                description=request_body.description,
                group_id=request_body.group_id,
            )
        except RepositoryError as e:
            raise DatabaseError(detail=str(e))

    async def update_device(
        self,
        company_id: UUID,
        device_id: UUID,
        request_body: UpdateDeviceRequestBody,
    ) -> UpdateDeviceResponse:
        try:
            return await self.device_repo.update_device(
                company_id=company_id,
                device_id=device_id,
                assigned_firmware_id=request_body.assigned_firmware_id,
                serial_number=request_body.serial_number,
                group_id=request_body.group_id,
                description=request_body.description,
                name=request_body.name,
            )
        except RepositoryError as e:
            raise DatabaseError(detail=str(e))

    async def delete_device(self, company_id: UUID, device_id: UUID) -> None:
        try:
            return await self.device_repo.delete_device(
                company_id=company_id, device_id=device_id
            )
        except RepositoryError as e:
            raise DatabaseError(detail=str(e))


def get_device_service(device_repo: DeviceRepositoryType) -> IDeviceService:
    return DeviceService(device_repo=device_repo)


DeviceServiceType = Annotated[IDeviceService, Depends(get_device_service)]
