from abc import ABC, abstractmethod
from typing import Annotated
from uuid import UUID

from calypte_api.firmware.repository import FirmwareRepoType, IFirmwareRepo
from calypte_api.firmware.schemas import DownloadFirmwareResponse

from fastapi import Depends, UploadFile


class IFirmwareService(ABC):
    @abstractmethod
    async def get_firmware_by_id(
        self, company_id: UUID, firmware_id: UUID
    ) -> DownloadFirmwareResponse:
        """
        Get firmware by id

        Args:
            firmware_id (UUID): firmware id
            company_id (UUID): user id

        """

    @abstractmethod
    async def upload_firmware(
        self, company_id: UUID, firmware_id: UUID, firmware: UploadFile
    ) -> None:
        """
        Upload firmware

        Args:
            company_id (UUID): user id
            firmware_id (UUID): firmware id
            firmware (UploadFile): firmware
        """


class FirmwareService(IFirmwareService):
    def __init__(self, firmware_repo: IFirmwareRepo):
        self.firmware_repo = firmware_repo

    async def get_firmware_by_id(
        self, company_id: UUID, firmware_id: UUID
    ) -> DownloadFirmwareResponse:
        firmware_generator = self.firmware_repo.get_firmware_by_id(
            company_id=company_id, firmware_id=firmware_id
        )
        return DownloadFirmwareResponse(firmware_generator)

    async def upload_firmware(
        self,
        company_id: UUID,
        firmware_id: UUID,
        firmware: UploadFile,
    ) -> None:
        await self.firmware_repo.upload_firmware(
            company_id=company_id, firmware_id=firmware_id, firmware=firmware
        )


def get_firmware_service(firmware_repo: FirmwareRepoType) -> IFirmwareService:
    return FirmwareService(firmware_repo=firmware_repo)


FirmwareServiceType = Annotated[
    IFirmwareService,
    Depends(get_firmware_service),
]
