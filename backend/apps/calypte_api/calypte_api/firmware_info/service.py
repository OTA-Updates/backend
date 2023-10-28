from abc import ABC, abstractmethod
from typing import Annotated
from uuid import UUID

from calypte_api.firmware_info.repository import (
    FirmwareInfoRepositoryType,
    IFirmwareInfoRepo,
)
from calypte_api.firmware_info.schemas import (
    FirmwareInfoUpdateRequestBody,
    FirmwareInfoUpdateResponse,
    GetFirmwareInfoQueryParams,
    GetFirmwareInfoResponse,
)

from fastapi import Depends
from fastapi_pagination import Page


class IFirmwareService(ABC):
    @abstractmethod
    async def get_firmware_info(
        self,
        user_id: UUID,
        firmware_id: UUID,
    ) -> GetFirmwareInfoResponse:
        """
        Get firmware by id

        Args:
            user_id (UUID): user id
            firmware_id (UUID): firmware id

        """

    @abstractmethod
    async def get_firmware_list(
        self, user_id: UUID, query_params: GetFirmwareInfoQueryParams
    ) -> Page[GetFirmwareInfoResponse]:
        """
        Get all firmwares

        Args:
            user_id (UUID): user id

        """

    @abstractmethod
    async def update_firmware(
        self,
        user_id: UUID,
        firmware_id: UUID,
        request_body: FirmwareInfoUpdateRequestBody,
    ) -> FirmwareInfoUpdateResponse:
        """
        Update firmware

        Args:
            user_id (UUID): user id
            firmware_id (UUID): firmware id
            request_body (CreateFirmwareRequestBody): request body
        """


class FirmwareService(IFirmwareService):
    def __init__(self, firmware_repo: IFirmwareInfoRepo):
        self.firmware_repo = firmware_repo

    async def get_firmware_info(
        self,
        user_id: UUID,
        firmware_id: UUID,
    ) -> GetFirmwareInfoResponse:
        return await self.firmware_repo.get_firmware_by_id(
            user_id=user_id,
            firmware_id=firmware_id,
        )

    async def get_firmware_list(
        self, user_id: UUID, query_params: GetFirmwareInfoQueryParams
    ) -> Page[GetFirmwareInfoResponse]:
        firmware_list = await self.firmware_repo.get_firmware_list(
            user_id=user_id,
            query_params=query_params,
        )
        return Page.create(
            items=firmware_list,
            params=query_params,
            total=query_params.size,
        )

    async def update_firmware(
        self,
        user_id: UUID,
        firmware_id: UUID,
        request_body: FirmwareInfoUpdateRequestBody,
    ) -> FirmwareInfoUpdateResponse:
        return await self.firmware_repo.update_firmware(
            user_id=user_id,
            firmware_id=firmware_id,
            name=request_body.name,
            description=request_body.description,
            version=request_body.version,
        )


def get_firmware_info_service(
    firmware_repo: FirmwareInfoRepositoryType
) -> IFirmwareInfoRepo:
    return FirmwareService(firmware_repo=firmware_repo)


FirmwareInfoServiceType = Annotated[
    IFirmwareService,
    Depends(get_firmware_info_service),
]
