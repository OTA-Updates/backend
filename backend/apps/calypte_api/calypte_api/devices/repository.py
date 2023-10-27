import random

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from calypte_api.common.dependencies import DBSessionType
from calypte_api.devices.schemas import (
    CreateDeviceResponse,
    GetDeviceQueryParams,
    GetDeviceResponse,
    UpdateDeviceResponse,
)

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


class IDeviceRepo(ABC):
    @abstractmethod
    async def get_device_by_id(
        self, user_id: UUID, device_id: UUID
    ) -> GetDeviceResponse:
        """
        Get device by id

        Args:
            device_id (UUID): device id
            user_id (UUID): user id

        """

    @abstractmethod
    async def get_devices(
        self, user_id: UUID, query_params: GetDeviceQueryParams
    ) -> list[GetDeviceResponse]:
        """
        Get devices by query params

        Args:
            user_id (UUID): user id
            query_params (GetDeviceQueryParams): query params
        """

    @abstractmethod
    async def create_device(
        self,
        name: str,
        user_id: UUID,
        tags: list[UUID],
    ) -> CreateDeviceResponse:
        """
        Create device

        Args:
            user_id (UUID): user id
            name (str): device name
            tags (list[UUID]): device tags
        """

    @abstractmethod
    async def update_device(
        self, user_id: UUID, device_id: UUID, name: str, tags: list[UUID]
    ) -> UpdateDeviceResponse:
        """
        Update device

        Args:
            user_id (UUID): user id
            device_id (UUID): device id
            name (str): device name
            tags (list[UUID]): device tags
        """

    @abstractmethod
    async def delete_device(self, user_id: UUID, device_id: UUID) -> None:
        """
        Delete device

        Args:
            user_id (UUID): user id
            device_id (UUID): device id
        """


class DeviceRepo(IDeviceRepo):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    # TODO: implement
    async def get_device_by_id(
        self, user_id: UUID, device_id: UUID
    ) -> GetDeviceResponse:
        return GetDeviceResponse(
            id=device_id,
            name="mocked device name",
            tags=[uuid4(), uuid4(), uuid4()],
            registered_at=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    # TODO: implement
    async def get_devices(
        self, user_id: UUID, query_params: GetDeviceQueryParams
    ) -> list[GetDeviceResponse]:
        tags = [uuid4() for _ in range(10)]
        return [
            GetDeviceResponse(
                id=uuid4(),
                name="mocked device name 1",
                tags=[random.choice(tags) for _ in range(random.randint(1, 3))],
                registered_at=None if random.randint(0, 1) == 0 else datetime.now(),
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            for i in range(query_params.size)
        ]

    # TODO: implement
    async def create_device(
        self,
        user_id: UUID,
        name: str,
        tags: list[UUID],
    ) -> CreateDeviceResponse:
        return CreateDeviceResponse(
            id=uuid4(),
            name=name,
            tags=tags,
            registered_at=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    # TODO: implement
    async def update_device(
        self, user_id: UUID, device_id: UUID, name: str, tags: list[UUID]
    ) -> UpdateDeviceResponse:
        registered_at = None if random.randint(0, 1) == 0 else datetime.now()
        return UpdateDeviceResponse(
            id=device_id,
            name=name,
            tags=tags,
            registered_at=registered_at,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    # TODO: implement
    async def delete_device(self, user_id: UUID, device_id: UUID) -> None:
        return None


def get_device_repo(db_session: DBSessionType) -> IDeviceRepo:
    return DeviceRepo(db_session=db_session)


DeviceRepositoryType = Annotated[IDeviceRepo, Depends(get_device_repo)]
