from abc import ABC, abstractmethod
from typing import Annotated, cast
from uuid import UUID

from calypte_api.common.dependencies import DBSessionType
from calypte_api.common.models import device_tag_lookup
from calypte_api.devices.models import Device
from calypte_api.devices.schemas import (
    CreateDeviceResponse,
    GetDeviceResponse,
    UpdateDeviceResponse,
)
from calypte_api.tags.models import Tag

from fastapi import Depends
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
        tags: list[UUID] | None,
        firmware_info_id: UUID | None,
        name: str | None,
        offset: int,
        limit: int,
    ) -> list[GetDeviceResponse]:
        """
        Get devices by query params

        Args:
            company_id (UUID): user id
            tags (list[UUID]): device tags
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
        description: str | None,
        firmware_info_id: UUID | None,
        tags: list[UUID] | None,
    ) -> CreateDeviceResponse:
        """
        Create device

        Args:
            company_id (UUID): user id
            name (str): device name
            tags (list[UUID]): device tags
        """

    @abstractmethod
    async def update_device(
        self,
        device_id: UUID,
        company_id: UUID,
        firmware_info_id: UUID | None,
        name: str | None,
        description: str | None,
        tags: list[UUID] | None,
    ) -> UpdateDeviceResponse:
        """
        Update device

        Args:
            company_id (UUID): user id
            device_id (UUID): device id
            name (str): device name
            tags (list[UUID]): device tags
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
            .join(Device.tags, isouter=True)
            .where(Device.company_id == company_id)
            .where(Device.id == device_id)
        )
        result = await self.db_session.scalar(select_stmt)

        if result is None:
            return None

        tags = [tag.id for tag in result.tags]
        return GetDeviceResponse(
            id=result.id,
            name=result.name,
            description=result.description,
            registered_at=result.registered_at,
            company_id=result.company_id,
            type_id=result.type_id,
            tags=tags,
            firmware_info_id=result.firmware_info_id,
            created_at=result.created_at,
            updated_at=result.updated_at,
        )

    async def get_devices(
        self,
        company_id: UUID,
        type_id: UUID | None,
        tags: list[UUID] | None,
        firmware_info_id: UUID | None,
        name: str | None,
        offset: int,
        limit: int,
    ) -> list[GetDeviceResponse]:
        select_stmt = (
            select(Device)
            .join(Device.tags, isouter=True)
            .where(Device.company_id == company_id)
            .order_by(Device.created_at)
        )

        if firmware_info_id is not None:
            select_stmt = select_stmt.where(
                Device.firmware_info_id == firmware_info_id
            )

        if tags is not None:
            select_stmt = select_stmt.where(Tag.id.in_(tags))

        if type_id is not None:
            select_stmt = select_stmt.where(Device.type_id == type_id)

        if name is not None:
            select_stmt = select_stmt.where(Device.name == name)

        select_stmt = (
            select_stmt.group_by(Device.id).offset(offset).limit(limit)
        )

        results = await self.db_session.scalars(select_stmt)

        get_devices_schemas = [
            GetDeviceResponse(
                id=result.id,
                name=result.name,
                description=result.description,
                registered_at=result.registered_at,
                company_id=result.company_id,
                type_id=result.type_id,
                tags=[tag.id for tag in result.tags],
                firmware_info_id=result.firmware_info_id,
                created_at=result.created_at,
                updated_at=result.updated_at,
            )
            for result in results.unique()
        ]

        return get_devices_schemas

    async def create_device(
        self,
        type_id: UUID,
        company_id: UUID,
        name: str,
        description: str | None,
        firmware_info_id: UUID | None,
        tags: list[UUID] | None,
    ) -> CreateDeviceResponse:
        insert_device_stmt = (
            insert(Device)
            .values(
                {
                    Device.type_id: type_id,
                    Device.firmware_info_id: firmware_info_id,
                    Device.name: name,
                    Device.description: description,
                    Device.company_id: company_id,
                }
            )
            .returning(Device)
        )
        device_result = await self.db_session.execute(insert_device_stmt)
        new_device = cast(Device, device_result.scalar())

        if tags is not None:
            tag_device_lookup_values = [
                {"device_id": new_device.id, "tag_id": tag_id}
                for tag_id in tags
            ]
            insert_device_tags_stmt = insert(device_tag_lookup).values(
                tag_device_lookup_values
            )
            await self.db_session.execute(insert_device_tags_stmt)

        return CreateDeviceResponse(
            id=new_device.id,
            name=new_device.name,
            description=new_device.description,
            registered_at=new_device.registered_at,
            company_id=new_device.company_id,
            type_id=new_device.type_id,
            tags=[tag.id for tag in await new_device.awaitable_attrs.tags],
            firmware_info_id=new_device.firmware_info_id,
            created_at=new_device.created_at,
            updated_at=new_device.updated_at,
        )

    async def update_device(
        self,
        device_id: UUID,
        company_id: UUID,
        firmware_info_id: UUID | None,
        name: str | None,
        description: str | None,
        tags: list[UUID] | None,
    ) -> UpdateDeviceResponse:
        if tags is not None:
            delete_device_tags_stmt = delete(device_tag_lookup).where(
                device_tag_lookup.c.device_id == device_id
            )
            await self.db_session.execute(delete_device_tags_stmt)

            insert_device_tags_stmt = device_tag_lookup.insert().values(
                [{"device_id": device_id, "tag_id": tag_id} for tag_id in tags]
            )
            await self.db_session.execute(insert_device_tags_stmt)

        insert_device_stmt = (
            update(Device)
            .where(Device.company_id == company_id)
            .where(Device.id == device_id)
            .values(
                id=device_id,
                name=name,
                description=description,
                company_id=company_id,
                firmware_info_id=firmware_info_id,
            )
            .returning(Device)
        )
        device_result = await self.db_session.execute(insert_device_stmt)
        new_device = device_result.scalar()

        return UpdateDeviceResponse(
            id=new_device.id,
            name=new_device.name,
            description=new_device.description,
            registered_at=new_device.registered_at,
            company_id=new_device.company_id,
            type_id=new_device.type_id,
            tags=[tag.id for tag in await new_device.awaitable_attrs.tags],
            firmware_info_id=new_device.firmware_info_id,
            created_at=new_device.created_at,
            updated_at=new_device.updated_at,
        )

    async def delete_device(self, company_id: UUID, device_id: UUID) -> None:
        delete_stmt = (
            delete(Device)
            .where(Device.company_id == company_id)
            .where(Device.id == device_id)
        )
        await self.db_session.execute(delete_stmt)


def get_device_repo(db_session: DBSessionType) -> IDeviceRepo:
    return DeviceRepo(db_session=db_session)


DeviceRepositoryType = Annotated[IDeviceRepo, Depends(get_device_repo)]
