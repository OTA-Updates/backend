from abc import ABC, abstractmethod
from typing import Annotated, cast
from uuid import UUID

from calypte_api.common.dependencies import DBSessionType
from calypte_api.common.exceptions import RepositoryError
from calypte_api.devices.models import Device
from calypte_api.devices.schemas import (
    CreateDeviceResponse,
    GetDeviceResponse,
    UpdateDeviceResponse,
)

from fastapi import Depends
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
        type_id: UUID | None,
        group_id: UUID | None,
        serial_number: str | None,
        current_firmware_id: UUID | None,
        name: str | None,
        offset: int,
        limit: int,
    ) -> list[GetDeviceResponse]:
        """
        Get devices by query params

        Args:
            company_id (UUID): user id
            type_id (UUID | None): type id
            tags (list[UUID]): device tags
            serial_number (str | None): device serial number
            current_firmware_id (UUID | None): current firmware id
            name (str | None): device name
            offset (int): offset
            limit (int): limit
        """

    @abstractmethod
    async def create_device(
        self,
        type_id: UUID,
        company_id: UUID,
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

    async def get_devices(
        self,
        company_id: UUID,
        type_id: UUID | None,
        group_id: UUID | None,
        serial_number: str | None,
        current_firmware_id: UUID | None,
        name: str | None,
        offset: int,
        limit: int,
    ) -> list[GetDeviceResponse]:
        select_stmt = select(Device).where(Device.company_id == company_id)

        if serial_number is not None:
            select_stmt = select_stmt.where(
                Device.serial_number == serial_number
            )
        if current_firmware_id is not None:
            select_stmt = select_stmt.where(
                Device.current_firmware_id == current_firmware_id
            )
        if group_id is not None:
            select_stmt = select_stmt.where(Device.group_id == group_id)
        if type_id is not None:
            select_stmt = select_stmt.where(Device.type_id == type_id)
        if name is not None:
            select_stmt = select_stmt.where(Device.name == name)

        select_stmt = (
            select_stmt.order_by(Device.created_at).offset(offset).limit(limit)
        )

        device_models = await self.db_session.scalars(select_stmt)

        get_devices_schemas = [
            GetDeviceResponse.model_validate(device_model)
            for device_model in device_models
        ]

        return get_devices_schemas

    async def create_device(
        self,
        type_id: UUID,
        company_id: UUID,
        name: str,
        serial_number: str,
        group_id: UUID,
        description: str | None,
    ) -> CreateDeviceResponse:
        insert_device_stmt = (
            insert(Device)
            .values(
                {
                    Device.type_id: type_id,
                    Device.group_id: group_id,
                    Device.name: name,
                    Device.description: description,
                    Device.company_id: company_id,
                    Device.serial_number: serial_number,
                }
            )
            .returning(Device)
        )

        try:
            device_result = await self.db_session.execute(insert_device_stmt)
            new_device = cast(Device, device_result.scalar())
            await self.db_session.commit()
        except IntegrityError as e:
            raise RepositoryError("Integrity error") from e

        return CreateDeviceResponse.model_validate(new_device)

    async def update_device(
        self,
        device_id: UUID,
        company_id: UUID,
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
                group_id=group_id,
                company_id=company_id,
                serial_number=serial_number,
            )
            .returning(Device)
        )

        try:
            device_result = await self.db_session.execute(insert_device_stmt)
            new_device = cast(Device, device_result.scalar())
            await self.db_session.commit()
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
            await self.db_session.commit()
        except IntegrityError as e:
            raise RepositoryError("Integrity error") from e


def get_device_repo(db_session: DBSessionType) -> IDeviceRepo:
    return DeviceRepo(db_session=db_session)


DeviceRepositoryType = Annotated[IDeviceRepo, Depends(get_device_repo)]
