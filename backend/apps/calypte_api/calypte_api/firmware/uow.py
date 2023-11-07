from types import TracebackType
from typing import Annotated, Self

from calypte_api.common.dependencies import DBSessionType, S3ClientType
from calypte_api.common.uow import IUOW
from calypte_api.firmware.repositories import (
    IFirmwareInfoRepo,
    IFirmwareS3Repo,
    get_firmware_info_repo,
    get_firmware_s3_repo,
)

from fastapi import Depends
from miniopy_async import Minio
from sqlalchemy.ext.asyncio import AsyncSession


class IUOWFirmware(IUOW):
    s3_repo: IFirmwareS3Repo
    sql_repo: IFirmwareInfoRepo


class UOWFirmware(IUOWFirmware):
    def __init__(self, sql_session: AsyncSession, s3_session: Minio) -> None:
        self.sql_session = sql_session
        self.s3_session = s3_session
        self.s3_repo = get_firmware_s3_repo(self.s3_session)
        self.sql_repo = get_firmware_info_repo(self.sql_session)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[Exception],
        exc_val: Exception,
        exc_tb: TracebackType,
    ):
        if exc_val is not None:
            await self.rollback()
            raise exc_val

    async def commit(self):
        await self.sql_session.commit()

    async def rollback(self):
        await self.sql_session.rollback()


def get_firmware_uow_service(
    s3_client: S3ClientType, sql_session: DBSessionType
) -> IUOWFirmware:
    return UOWFirmware(sql_session=sql_session, s3_session=s3_client)


FirmwareUOWType = Annotated[IUOWFirmware, Depends(get_firmware_uow_service)]
