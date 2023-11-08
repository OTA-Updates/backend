from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import cast
from uuid import UUID

from calypte_api.common.exceptions import RepositoryError
from calypte_api.devices.models import Device
from calypte_api.devices.schemas import (
    CreateDeviceResponse,
    DeviceFilter,
    GetDeviceResponse,
    UpdateDeviceResponse,
)

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import delete, insert, select, update


class IDeviceRepo(ABC):
    @abstractmethod
    async def get_device_by_id(
        self, company_id: UUID, device_id: UUID
    ) -> GetDeviceResponse | None:
        """
        Get device by id

        Args:
            device_id (UUID): device id
            company_id (UUID): user id

        """

    @abstractmethod
    async def get_devices(
        self,
        company_id: UUID,
        pagination_params: Params,
        filtration_params: DeviceFilter,
    ) -> list[GetDeviceResponse]:
        """
        Get devices by query params

        Args:
            company_id (UUID): user id
            pagination_params (Params): pagination params
            filtration_params (DeviceFilter): filtration params
        """

    @abstractmethod
    async def create_device(
        self,
        type_id: UUID,
        company_id: UUID,
        assigned_firmware_id: UUID,
        name: str,
        serial_number: str,
        group_id: UUID,
        description: str | None,
    ) -> CreateDeviceResponse:
        """
        Create device

        Args:
            type_id (UUID): type id
            company_id (UUID): user id
            assigned_firmware_id (UUID): assigned firmware id
            name (str): device name
            description (str | None): device description
            serial_number (str): device serial number
            group_id (UUID): group id
        """

    @abstractmethod
    async def update_device(
        self,
        device_id: UUID,
        company_id: UUID,
        assigned_firmware_id: UUID,
        group_id: UUID,
        serial_number: str,
        name: str,
        description: str | None,
    ) -> UpdateDeviceResponse:
        """
        Update device

        Args:
            device_id (UUID): device id
            company_id (UUID): user id
            assigned_firmware_id (UUID): assigned firmware id
            name (str): device name
            serial_number (str): device serial number
            group_id (UUID): group id
            description (str | None): device description
        """

    @abstractmethod
    async def delete_device(self, company_id: UUID, device_id: UUID) -> None:
        """
        Delete device

        Args:
            company_id (UUID): user id
            device_id (UUID): device id
        """


class DeviceRepo(IDeviceRepo):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def get_device_by_id(
        self, company_id: UUID, device_id: UUID
    ) -> GetDeviceResponse | None:
        select_stmt = (
            select(Device)
            .where(Device.company_id == company_id)
            .where(Device.id == device_id)
        )
        device_model = await self.db_session.scalar(select_stmt)

        if device_model is None:
            return None

        return GetDeviceResponse.model_validate(device_model)

    def _transformer(
        self, device: Sequence[Device]
    ) -> list[GetDeviceResponse]:
        return [GetDeviceResponse.model_validate(model) for model in device]

    async def get_devices(
        self,
        company_id: UUID,
        pagination_params: Params,
        filtration_params: DeviceFilter,
    ) -> list[GetDeviceResponse]:
        select_stmt = select(Device).where(Device.company_id == company_id)
        select_stmt = filtration_params.filter(select_stmt)
        select_stmt = filtration_params.sort(select_stmt)

        get_devices_schemas = await paginate(
            self.db_session,
            select_stmt,
            params=pagination_params,
            transformer=self._transformer,
        )

        return get_devices_schemas

    async def create_device(
        self,
        type_id: UUID,
        company_id: UUID,
        assigned_firmware_id: UUID,
        name: str,
        serial_number: str,
        group_id: UUID,
        description: str | None,
    ) -> CreateDeviceResponse:
        insert_device_stmt = (
            insert(Device)
            .values(
                type_id=type_id,
                group_id=group_id,
                assigned_firmware_id=assigned_firmware_id,
                name=name,
                description=description,
                company_id=company_id,
                serial_number=serial_number,
            )
            .returning(Device)
        )

        try:
            device_result = await self.db_session.execute(insert_device_stmt)
            new_device = cast(Device, device_result.scalar())
        except IntegrityError as e:
            raise RepositoryError("Integrity error") from e

        return CreateDeviceResponse.model_validate(new_device)

    async def update_device(
        self,
        device_id: UUID,
        company_id: UUID,
        assigned_firmware_id: UUID,
        group_id: UUID,
        serial_number: str,
        name: str,
        description: str | None,
    ) -> UpdateDeviceResponse:
        insert_device_stmt = (
            update(Device)
            .where(Device.company_id == company_id)
            .where(Device.id == device_id)
            .values(
                id=device_id,
                name=name,
                description=description,
                assigned_firmware_id=assigned_firmware_id,
                group_id=group_id,
                company_id=company_id,
                serial_number=serial_number,
            )
            .returning(Device)
        )

        try:
            device_result = await self.db_session.execute(insert_device_stmt)
            new_device = cast(Device, device_result.scalar())
        except IntegrityError as e:
            raise RepositoryError("Integrity error") from e

        return UpdateDeviceResponse.model_validate(new_device)

    async def delete_device(self, company_id: UUID, device_id: UUID) -> None:
        delete_stmt = (
            delete(Device)
            .where(Device.company_id == company_id)
            .where(Device.id == device_id)
        )

        try:
            await self.db_session.execute(delete_stmt)
        except IntegrityError as e:
            raise RepositoryError("Integrity error") from e


def get_device_repo(db_session: AsyncSession) -> IDeviceRepo:
    return DeviceRepo(db_session=db_session)
