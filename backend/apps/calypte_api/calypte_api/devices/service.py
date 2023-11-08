from abc import ABC, abstractmethod
from typing import Annotated
from uuid import UUID

from calypte_api.common.exceptions import (
    ObjectNotFoundError,
)
from calypte_api.devices.schemas import (
    CreateDeviceRequestBody,
    CreateDeviceResponse,
    DeviceFilter,
    GetDeviceResponse,
    UpdateDeviceRequestBody,
    UpdateDeviceResponse,
)
from calypte_api.devices.uow import IUOWDevices, UOWDeviceType
from calypte_api.firmware.validators import validate_firmware_id
from calypte_api.groups.validators import validate_group_id
from calypte_api.types.validators import validate_type_id

from fastapi import Depends
from fastapi_pagination import Page, Params


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
        self,
        company_id: UUID,
        pagination_params: Params,
        filtration_params: DeviceFilter,
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
    def __init__(self, uow: IUOWDevices):
        self.uow = uow

    async def get_device(
        self,
        company_id: UUID,
        device_id: UUID,
    ) -> GetDeviceResponse:
        device_schema = await self.uow.device_repo.get_device_by_id(
            company_id=company_id, device_id=device_id
        )

        if device_schema is None:
            raise ObjectNotFoundError(object_id=device_id)

        return device_schema

    async def get_devices(
        self,
        company_id: UUID,
        pagination_params: Params,
        filtration_params: DeviceFilter,
    ) -> Page[GetDeviceResponse]:
        devices_page = await self.uow.device_repo.get_devices(
            company_id=company_id,
            pagination_params=pagination_params,
            filtration_params=filtration_params,
        )
        return devices_page

    async def create_device(
        self, company_id: UUID, request_body: CreateDeviceRequestBody
    ) -> CreateDeviceResponse:
        async with self.uow as uow:
            await validate_type_id(
                type_repo=uow.type_repo,
                type_id=request_body.type_id,
                company_id=company_id,
            )
            await validate_group_id(
                group_repo=uow.group_repo,
                type_id=request_body.type_id,
                group_id=request_body.group_id,
                company_id=company_id,
            )
            await validate_firmware_id(
                firmware_repo=uow.firmware_repo,
                type_id=request_body.type_id,
                firmware_id=request_body.assigned_firmware_id,
                company_id=company_id,
            )

            created_device = await uow.device_repo.create_device(
                type_id=request_body.type_id,
                company_id=company_id,
                assigned_firmware_id=request_body.assigned_firmware_id,
                serial_number=request_body.serial_number,
                name=request_body.name,
                description=request_body.description,
                group_id=request_body.group_id,
            )
            await uow.commit()
            return created_device

    async def update_device(
        self,
        company_id: UUID,
        device_id: UUID,
        request_body: UpdateDeviceRequestBody,
    ) -> UpdateDeviceResponse:
        async with self.uow as uow:
            device = await self.uow.device_repo.get_device_by_id(
                company_id=company_id, device_id=device_id
            )
            if device is None:
                raise ObjectNotFoundError(object_id=device_id)

            await validate_group_id(
                group_repo=uow.group_repo,
                type_id=device.type_id,
                group_id=request_body.group_id,
                company_id=company_id,
            )
            await validate_firmware_id(
                firmware_repo=uow.firmware_repo,
                type_id=device.type_id,
                firmware_id=request_body.assigned_firmware_id,
                company_id=company_id,
            )

            updated_device = await uow.device_repo.update_device(
                company_id=company_id,
                device_id=device_id,
                assigned_firmware_id=request_body.assigned_firmware_id,
                serial_number=request_body.serial_number,
                group_id=request_body.group_id,
                description=request_body.description,
                name=request_body.name,
            )
            await uow.commit()
            return updated_device

    async def delete_device(self, company_id: UUID, device_id: UUID) -> None:
        async with self.uow as uow:
            await self.uow.device_repo.delete_device(
                company_id=company_id, device_id=device_id
            )
            await uow.commit()


def get_device_service(uow: UOWDeviceType) -> IDeviceService:
    return DeviceService(uow=uow)


DeviceServiceType = Annotated[IDeviceService, Depends(get_device_service)]
