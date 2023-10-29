from abc import ABC, abstractmethod
from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from calypte_api.common.dependencies import DBSessionType
from calypte_api.firmware_info.schemas import (
    CreateFirmwareInfoResponse,
    GetFirmwareInfoQueryParams,
    GetFirmwareInfoResponse,
    UpdateFirmwareInfoResponse,
)

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


class IFirmwareInfoRepo(ABC):
    @abstractmethod
    async def get_firmware_by_id(
        self,
        user_id: UUID,
        firmware_id: UUID,
    ) -> GetFirmwareInfoResponse:
        """
        Get firmware by id

        Args:
            firmware_id (UUID): firmware id
            user_id (UUID): user id

        """

    @abstractmethod
    async def get_firmware_list(
        self, user_id: UUID, query_params: GetFirmwareInfoQueryParams
    ) -> list[GetFirmwareInfoResponse]:
        """
        Get firmwares by query params

        Args:
            user_id (UUID): user id
            query_params (GetFirmwareQueryParams): query params
        """

    @abstractmethod
    async def update_firmware(
        self,
        user_id: UUID,
        firmware_id: UUID,
        name: str,
        description: str,
        version: str,
    ) -> UpdateFirmwareInfoResponse:
        """
        Update firmware

        Args:
            user_id (UUID): user id
            firmware_id (UUID): firmware id
            name (str): firmware name
            description (str): firmware description
        """

    @abstractmethod
    async def create_firmware(
        self,
        name: str,
        description: str,
        version: str,
        user_id: UUID,
    ) -> CreateFirmwareInfoResponse:
        """
        Create firmware

        Args:
            user_id (UUID): user id
            name (str): firmware name
            description (str): firmware description
        """


class FirmwareInfoRepo(IFirmwareInfoRepo):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    # TODO: implement
    async def get_firmware_by_id(
        self,
        user_id: UUID,
        firmware_id: UUID,
    ) -> GetFirmwareInfoResponse:
        return GetFirmwareInfoResponse(
            id=firmware_id,
            name="mocked firmware name",
            description="mocked firmware description",
            version="mocked firmware version",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    # TODO: implement
    async def get_firmware_list(
        self, user_id: UUID, query_params: GetFirmwareInfoQueryParams
    ) -> list[GetFirmwareInfoResponse]:
        return [
            GetFirmwareInfoResponse(
                id=uuid4(),
                name="mocked firmware name",
                description="mocked firmware description",
                version="mocked firmware version",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            for i in range(query_params.size)
        ]

    # TODO: implement
    async def update_firmware(
        self,
        user_id: UUID,
        firmware_id: UUID,
        name: str,
        description: str,
        version: str,
    ) -> UpdateFirmwareInfoResponse:
        return UpdateFirmwareInfoResponse(
            id=firmware_id,
            name=name,
            description=description,
            version=version,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    async def create_firmware(
        self,
        name: str,
        description: str,
        version: str,
        user_id: UUID,
    ) -> CreateFirmwareInfoResponse:
        return CreateFirmwareInfoResponse(
            id=uuid4(),
            name=name,
            description=description,
            version=version,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )


def get_firmware_info_repo(db_session: DBSessionType) -> IFirmwareInfoRepo:
    return FirmwareInfoRepo(db_session=db_session)


FirmwareInfoRepositoryType = Annotated[
    IFirmwareInfoRepo, Depends(get_firmware_info_repo)
]
