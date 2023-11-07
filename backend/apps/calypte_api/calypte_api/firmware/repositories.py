from abc import ABC, abstractmethod
from collections.abc import Coroutine, Iterable
from typing import Any
from uuid import UUID

from calypte_api.firmware.models import FirmwareInfo
from calypte_api.firmware.schemas import (
    CreateFirmwareResponse,
    GetFirmwareInfoResponse,
    UpdateFirmwareInfoResponse,
)

import aiohttp

from fastapi import UploadFile
from miniopy_async import Minio
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class IFirmwareS3Repo(ABC):
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


class IFirmwareInfoRepo(ABC):
    @abstractmethod
    async def get_firmware_by_id(
        self,
        company_id: UUID,
        firmware_id: UUID,
    ) -> GetFirmwareInfoResponse | None:
        """
        Get firmware by id

        Args:
            firmware_id (UUID): firmware id
            user_id (UUID): user id

        """

    @abstractmethod
    async def get_firmware_list(
        self,
        company_id: UUID,
        limit: int,
        offset: int,
        serial_number: str | None,
        type_id: UUID | None,
        version: str | None,
        name: str | None,
    ) -> list[GetFirmwareInfoResponse]:
        """
        Get firmware by query params

        Args:
            company_id (UUID): user id
            limit (int): limit
            offset (int): offset
            serial_number (str): firmware serial number
            type_id (UUID): type id
            version (str): firmware version
            name (str): firmware name
        """

    @abstractmethod
    async def update_firmware(
        self,
        company_id: UUID,
        firmware_id: UUID,
        serial_number: str,
        name: str,
        description: str,
        version: str,
    ) -> UpdateFirmwareInfoResponse:
        """
        Update firmware

        Args:
            company_id (UUID): user id
            firmware_id (UUID): firmware id
            serial_number (str): firmware serial number
            name (str): firmware name
            description (str): firmware description
            version (str): firmware version
        """

    @abstractmethod
    async def create_firmware(
        self,
        company_id: UUID,
        type_id: UUID,
        serial_number: str,
        name: str,
        description: str,
        version: str,
    ) -> CreateFirmwareResponse:
        """
        Create firmware

        Args:
            company_id (UUID): user id
            type_id (UUID): type id
            serial_number (str): firmware serial number
            name (str): firmware name
            description (str): firmware description
            version (str): firmware version
        """

    @abstractmethod
    async def check_firmware_belongs_to(
        self,
        firmware_id: UUID,
        type_id: UUID | None = None,
        company_id: UUID | None = None,
    ) -> bool:
        """
        Check firmware belongs to type and/or company

        Args:
            firmware_id (UUID): firmware id
            type_id (UUID): type id
            company_id (UUID): company id
        """


class FirmwareS3Repo(IFirmwareS3Repo):
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


class FirmwareInfoRepo(IFirmwareInfoRepo):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def get_firmware_by_id(
        self, company_id: UUID, firmware_id: UUID
    ) -> GetFirmwareInfoResponse | None:
        select_stmt = (
            select(FirmwareInfo)
            .where(FirmwareInfo.company_id == company_id)
            .where(FirmwareInfo.id == firmware_id)
        )
        firmware_info_model = await self.db_session.scalar(select_stmt)
        if firmware_info_model is None:
            return None

        return GetFirmwareInfoResponse.model_validate(firmware_info_model)

    async def get_firmware_list(
        self,
        company_id: UUID,
        limit: int,
        offset: int,
        serial_number: str | None,
        type_id: UUID | None,
        version: str | None,
        name: str | None,
    ) -> list[GetFirmwareInfoResponse]:
        select_stmt = select(FirmwareInfo).where(
            FirmwareInfo.company_id == company_id
        )
        if serial_number:
            select_stmt = select_stmt.where(
                FirmwareInfo.serial_number == serial_number
            )
        if type_id:
            select_stmt = select_stmt.where(FirmwareInfo.type_id == type_id)
        if name:
            select_stmt = select_stmt.where(FirmwareInfo.name == name)
        if version:
            select_stmt = select_stmt.where(FirmwareInfo.version == version)

        select_stmt = (
            select_stmt.order_by(FirmwareInfo.created_at)
            .limit(limit=limit)
            .offset(offset=offset)
        )
        firmware_info_models = await self.db_session.scalars(select_stmt)

        firmware_info_schemas = [
            GetFirmwareInfoResponse.model_validate(firmware_info)
            for firmware_info in firmware_info_models
        ]

        return firmware_info_schemas

    async def update_firmware(
        self,
        company_id: UUID,
        firmware_id: UUID,
        serial_number: str,
        name: str,
        description: str,
        version: str,
    ) -> UpdateFirmwareInfoResponse:
        update_stmt = (
            update(FirmwareInfo)
            .where(FirmwareInfo.id == firmware_id)
            .where(FirmwareInfo.company_id == company_id)
            .values(
                {
                    FirmwareInfo.serial_number: serial_number,
                    FirmwareInfo.name: name,
                    FirmwareInfo.description: description,
                    FirmwareInfo.version: version,
                }
            )
            .returning(FirmwareInfo)
        )
        firmware_info_model = await self.db_session.scalar(update_stmt)

        return UpdateFirmwareInfoResponse.model_validate(firmware_info_model)

    async def create_firmware(
        self,
        company_id: UUID,
        type_id: UUID,
        serial_number: str,
        name: str,
        description: str,
        version: str,
    ) -> CreateFirmwareResponse:
        create_stmt = (
            insert(FirmwareInfo)
            .values(
                {
                    FirmwareInfo.company_id: company_id,
                    FirmwareInfo.type_id: type_id,
                    FirmwareInfo.serial_number: serial_number,
                    FirmwareInfo.name: name,
                    FirmwareInfo.description: description,
                    FirmwareInfo.version: version,
                }
            )
            .returning(FirmwareInfo)
        )

        firmware_info_model = await self.db_session.scalar(create_stmt)

        return CreateFirmwareResponse.model_validate(firmware_info_model)

    async def check_firmware_belongs_to(
        self,
        firmware_id: UUID,
        type_id: UUID | None = None,
        company_id: UUID | None = None,
    ) -> bool:
        select_stmt = select(FirmwareInfo).where(
            FirmwareInfo.id == firmware_id
        )
        if type_id:
            select_stmt = select_stmt.where(FirmwareInfo.type_id == type_id)
        if company_id:
            select_stmt = select_stmt.where(
                FirmwareInfo.company_id == company_id
            )
        select_stmt = select_stmt

        firmware_info_model = await self.db_session.scalar(select_stmt)
        return bool(firmware_info_model)


def get_firmware_info_repo(db_session: AsyncSession) -> IFirmwareInfoRepo:
    return FirmwareInfoRepo(db_session=db_session)


def get_firmware_s3_repo(s3_client: Minio) -> IFirmwareS3Repo:
    return FirmwareS3Repo(s3_client)
