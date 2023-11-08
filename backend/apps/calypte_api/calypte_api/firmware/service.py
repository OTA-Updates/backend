from abc import ABC, abstractmethod
from typing import Annotated
from uuid import UUID

from calypte_api.common.exceptions import DatabaseError, ObjectNotFoundError
from calypte_api.firmware.commands import CreateFirmwareCommand
from calypte_api.firmware.schemas import (
    CreateFirmwareRequestBody,
    CreateFirmwareResponse,
    DownloadFirmwareResponse,
    FirmwareFilter,
    FirmwareInfoUpdateRequestBody,
    GetFirmwareInfoResponse,
    UpdateFirmwareInfoResponse,
)
from calypte_api.firmware.uow import (
    FirmwareUOWType,
    IUOWFirmware,
)

from fastapi import Depends
from fastapi_pagination import Page, Params


class IFirmwareService(ABC):
    @abstractmethod
    async def get_firmware(
        self, company_id: UUID, firmware_id: UUID
    ) -> DownloadFirmwareResponse:
        """
        Get firmware by id

        Args:
            firmware_id (UUID): firmware id
            company_id (UUID): user id

        """

    @abstractmethod
    async def create_firmware(
        self,
        company_id: UUID,
        request_body: CreateFirmwareRequestBody,
    ) -> CreateFirmwareResponse:
        """
        Upload firmware

        Args:
            company_id (UUID): user id
            request_body (CreateFirmwareRequestBody): request body
        """

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
    async def get_firmware_info_list(
        self,
        company_id: UUID,
        pagination_params: Params,
        filtration_params: FirmwareFilter,
    ) -> Page[GetFirmwareInfoResponse]:
        """
        Get all firmware

        Args:
            company_id (UUID): user id

        returns:
            list[GetFirmwareInfoResponse]: list of firmware info
        """

    @abstractmethod
    async def update_firmware_info(
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


class FirmwareService(IFirmwareService):
    def __init__(self, uow: IUOWFirmware) -> None:
        self.uow = uow

    async def get_firmware(
        self, company_id: UUID, firmware_id: UUID
    ) -> DownloadFirmwareResponse:
        firmware_generator = self.uow.firm_s3_repo.get_firmware_by_id(
            company_id=company_id, firmware_id=firmware_id
        )
        return DownloadFirmwareResponse(firmware_generator)  # type: ignore

    async def create_firmware(
        self,
        company_id: UUID,
        request_body: CreateFirmwareRequestBody,
    ) -> CreateFirmwareResponse:
        create_command = CreateFirmwareCommand(
            uow=self.uow,
            company_id=company_id,
            request_type=request_body,
        )
        try:
            return await create_command.execute()
        except Exception as e:
            await create_command.rollback()
            raise DatabaseError("Something went wrong") from e

    async def get_firmware_info(
        self,
        company_id: UUID,
        firmware_id: UUID,
    ) -> GetFirmwareInfoResponse:
        firmware_schema = await self.uow.firm_sql_repo.get_firmware_by_id(
            company_id=company_id,
            firmware_id=firmware_id,
        )

        if not firmware_schema:
            raise ObjectNotFoundError(object_id=firmware_id)

        return firmware_schema

    async def get_firmware_info_list(
        self,
        company_id: UUID,
        pagination_params: Params,
        filtration_params: FirmwareFilter,
    ) -> Page[GetFirmwareInfoResponse]:
        firmware_page = await self.uow.firm_sql_repo.get_firmware_list(
            company_id=company_id,
            pagination_params=pagination_params,
            filtration_params=filtration_params,
        )

        return firmware_page

    async def update_firmware_info(
        self,
        company_id: UUID,
        firmware_id: UUID,
        request_body: FirmwareInfoUpdateRequestBody,
    ) -> UpdateFirmwareInfoResponse:
        async with self.uow as uow:
            firmware_info = await uow.firm_sql_repo.update_firmware(
                company_id=company_id,
                serial_number=request_body.serial_number,
                firmware_id=firmware_id,
                name=request_body.name,
                description=request_body.description,
                version=request_body.version,
            )
            await uow.commit()

        return firmware_info


def get_firmware_info_service(uow: FirmwareUOWType) -> IFirmwareService:
    return FirmwareService(uow)


FirmwareServiceType = Annotated[
    IFirmwareService,
    Depends(get_firmware_info_service),
]
