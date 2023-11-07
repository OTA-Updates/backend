from abc import ABC, abstractmethod
from collections.abc import Coroutine, Iterable
from typing import Annotated, Any
from uuid import UUID

from calypte_api.common.dependencies import S3ClientType

import aiohttp

from fastapi import Depends, UploadFile
from miniopy_async import Minio


class IFirmwareRepo(ABC):
    @abstractmethod
    async def get_firmware_by_id(
        self,
        company_id: UUID,
        firmware_id: UUID,
    ) -> Iterable[bytes]:
        """
        Get firmware by id

        Args:
            firmware_id (UUID): firmware id
            company_id (UUID): user id

        """

    @abstractmethod
    async def upload_firmware(
        self,
        company_id: UUID,
        firmware_id: UUID,
        firmware: UploadFile,
    ) -> None:
        """
        Upload firmware

        Args:
            company_id (UUID): user id
            firmware_id (UUID): firmware id
            firmware (bytes): firmware
        """


class FirmwareRepo(IFirmwareRepo):
    CHUCK_SIZE_BYTES = 1024 * 1024 * 5  # 5MB

    def __init__(self, client: Minio):
        self.client = client

    async def get_firmware_by_id(
        self,
        company_id: UUID,
        firmware_id: UUID,
    ) -> Coroutine[Any, Any, Iterable[bytes]]:
        async with aiohttp.ClientSession() as session:
            firmware_info = await self.client.stat_object(
                bucket_name=str(company_id),
                object_name=str(firmware_id),
            )
            chunk_count = (firmware_info.size // self.CHUCK_SIZE_BYTES) + 1
            for i in range(chunk_count):
                response = await self.client.get_object(
                    bucket_name=str(company_id),
                    object_name=str(firmware_id),
                    offset=i * self.CHUCK_SIZE_BYTES,
                    length=self.CHUCK_SIZE_BYTES,
                    session=session,
                )
                yield await response.read()
            response.release()

    async def upload_firmware(
        self,
        company_id: UUID,
        firmware_id: UUID,
        firmware: UploadFile,
    ) -> None:
        bucket = await self.client.bucket_exists(str(company_id))
        if not bucket:
            await self.client.make_bucket(str(company_id))

        await self.client.put_object(
            bucket_name=str(company_id),
            object_name=str(firmware_id),
            data=firmware.file,
            length=firmware.size,
        )


def get_firmware_repo(s3_client: S3ClientType) -> IFirmwareRepo:
    return FirmwareRepo(s3_client)


FirmwareRepoType = Annotated[IFirmwareRepo, Depends(get_firmware_repo)]
