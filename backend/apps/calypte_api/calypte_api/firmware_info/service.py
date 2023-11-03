from abc import ABC, abstractmethod
from typing import Annotated
from uuid import UUID

from calypte_api.common.exeptions import ObjectNotFoundError
from calypte_api.firmware_info.repository import (
    FirmwareInfoRepositoryType,
    IFirmwareInfoRepo,
)
from calypte_api.firmware_info.schemas import (
    CreateFirmwareInfoRequestBody,
    CreateFirmwareInfoResponse,
    FirmwareInfoUpdateRequestBody,
    GetFirmwareInfoQueryParams,
    GetFirmwareInfoResponse,
    UpdateFirmwareInfoResponse,
)

from fastapi import Depends
from fastapi_pagination import Page


class IFirmwareService(ABC):
    @abstractmethod
    async def get_firmware_info(
        self,
        company_id: UUID,
        firmware_id: UUID,
    ) -> GetFirmwareInfoResponse:
        """
        Get firmware by id

        Args:
            company_id (UUID): user id
            firmware_id (UUID): firmware id

        """

    @abstractmethod
    async def get_firmware_list(
        self, company_id: UUID, query_params: GetFirmwareInfoQueryParams
    ) -> Page[GetFirmwareInfoResponse]:
        """
        Get all firmwares

        Args:
            company_id (UUID): user id

        returns:
            list[GetFirmwareInfoResponse]: list of firmware info
        """

    @abstractmethod
    async def update_firmware(
        self,
        company_id: UUID,
        firmware_id: UUID,
        request_body: FirmwareInfoUpdateRequestBody,
    ) -> UpdateFirmwareInfoResponse:
        """
        Update firmware

        Args:
            company_id (UUID): user id
            firmware_id (UUID): firmware id
            request_body (CreateFirmwareRequestBody): request body

        returns:
            UpdateFirmwareInfoResponse: updated firmware info
        """

    @abstractmethod
    async def create_firmware(
        self,
        company_id: UUID,
        request_body: CreateFirmwareInfoRequestBody,
    ) -> CreateFirmwareInfoResponse:
        """
        Create firmware

        Args:
            company_id (UUID): user id
            request_body (CreateFirmwareRequestBody): request body

        returns:
            CreateFirmwareInfoResponse: created firmware info
        """


class FirmwareService(IFirmwareService):
    def __init__(self, firmware_repo: IFirmwareInfoRepo):
        self.firmware_repo = firmware_repo

    async def get_firmware_info(
        self,
        company_id: UUID,
        firmware_id: UUID,
    ) -> GetFirmwareInfoResponse:
        firmware_schema = await self.firmware_repo.get_firmware_by_id(
            company_id=company_id,
            firmware_id=firmware_id,
        )

        if not firmware_schema:
            raise ObjectNotFoundError(object_id=firmware_id)

        return firmware_schema

    async def get_firmware_list(
        self, company_id: UUID, query_params: GetFirmwareInfoQueryParams
    ) -> Page[GetFirmwareInfoResponse]:
        limit = query_params.size
        offset = (query_params.page - 1) * limit

        firmware_list = await self.firmware_repo.get_firmware_list(
            company_id=company_id,
            serial_number=query_params.serial_number,
            offset=offset,
            limit=limit,
            type_id=query_params.type_id,
            name=query_params.name,
            version=query_params.version,
        )

        return Page.create(
            items=firmware_list,
            params=query_params,
            total=query_params.size,
        )

    async def update_firmware(
        self,
        company_id: UUID,
        firmware_id: UUID,
        request_body: FirmwareInfoUpdateRequestBody,
    ) -> UpdateFirmwareInfoResponse:
        return await self.firmware_repo.update_firmware(
            company_id=company_id,
            serial_number=request_body.serial_number,
            firmware_id=firmware_id,
            name=request_body.name,
            description=request_body.description,
            version=request_body.version,
        )

    async def create_firmware(
        self,
        company_id: UUID,
        request_body: CreateFirmwareInfoRequestBody,
    ) -> CreateFirmwareInfoResponse:
        return await self.firmware_repo.create_firmware(
            company_id=company_id,
            type_id=request_body.type_id,
            serial_number=request_body.serial_number,
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
