from abc import ABC, abstractmethod
from collections.abc import Generator
from typing import Annotated, BinaryIO
from uuid import UUID

from fastapi import Depends


class IFirmwareRepo(ABC):
    @abstractmethod
    async def get_firmware_by_id(
        self,
        user_id: UUID,
        firmware_id: UUID,
    ) -> Generator[None, None, str]:
        """
        Get firmware by id

        Args:
            firmware_id (UUID): firmware id
            user_id (UUID): user id

        """

    @abstractmethod
    async def upload_firmware(
        self,
        user_id: UUID,
        firmware_id: UUID,
        firmware: BinaryIO,
    ) -> None:
        """
        Upload firmware

        Args:
            user_id (UUID): user id
            firmware_id (UUID): firmware id
            firmware (bytes): firmware
        """


class FirmwareRepo(IFirmwareRepo):
    async def get_firmware_by_id(
        self,
        user_id: UUID,
        firmware_id: UUID,
    ) -> Generator[None, None, str]:
        with open(f"./{firmware_id}.txt") as f:
            for line in f:
                yield line

    async def upload_firmware(
        self,
        user_id: UUID,
        firmware_id: UUID,
        firmware: BinaryIO,
    ) -> None:
        with open(f"./{firmware_id}.txt", "w") as f:
            f.write(firmware.read().decode("utf-8"))


def get_firmware_repo() -> IFirmwareRepo:
    return FirmwareRepo()


FirmwareRepoType = Annotated[IFirmwareRepo, Depends(get_firmware_repo)]
