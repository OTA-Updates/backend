from abc import ABC, abstractmethod
from typing import Annotated
from uuid import UUID

from calypte_api.firmware.repository import FirmwareRepoType, IFirmwareRepo
from calypte_api.firmware.schemas import DownloadFirmwareResponse

from fastapi import Depends


class IFirmwareService(ABC):
    @abstractmethod
    async def get_firmware_by_id(
        self, user_id: UUID, firmware_id: UUID
    ) -> DownloadFirmwareResponse:
        """
        Get firmware by id

        Args:
            firmware_id (UUID): firmware id
            user_id (UUID): user id

        """

    @abstractmethod
    async def upload_firmware(
        self, user_id: UUID, firmware_id: UUID, firmware: bytes
    ) -> None:
        """
        Upload firmware

        Args:
            user_id (UUID): user id
            firmware_id (UUID): firmware id
            firmware (bytes): firmware
        """


class FirmwareService(IFirmwareService):
    def __init__(self, firmware_repo: IFirmwareRepo):
        self.firmware_repo = firmware_repo

    async def get_firmware_by_id(
        self, user_id: UUID, firmware_id: UUID
    ) -> DownloadFirmwareResponse:
        firmware_stream = self.firmware_repo.get_firmware_by_id(
            user_id=user_id, firmware_id=firmware_id
        )
        return DownloadFirmwareResponse(firmware_stream)

    async def upload_firmware(
        self,
        user_id: UUID,
        firmware_id: UUID,
        firmware: bytes,
    ) -> None:
        await self.firmware_repo.upload_firmware(
            user_id=user_id, firmware_id=firmware_id, firmware=firmware
        )


def get_firmware_service(firmware_repo: FirmwareRepoType) -> IFirmwareService:
    return FirmwareService(firmware_repo=firmware_repo)


FirmwareServiceType = Annotated[
    IFirmwareService,
    Depends(get_firmware_service),
]
