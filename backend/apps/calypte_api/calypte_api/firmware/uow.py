from typing import Annotated

from calypte_api.common.dependencies import DBSessionType, S3ClientType
from calypte_api.common.uow import IUOW, UOW
from calypte_api.firmware.repositories import (
    IFirmwareInfoRepo,
    IFirmwareS3Repo,
    get_firmware_info_repo,
    get_firmware_s3_repo,
)
from calypte_api.types.repositories import ITypeRepo, get_type_repo

from fastapi import Depends
from miniopy_async import Minio
from sqlalchemy.ext.asyncio import AsyncSession


class IUOWFirmware(IUOW):
    firm_s3_repo: IFirmwareS3Repo
    firm_sql_repo: IFirmwareInfoRepo
    type_repo: ITypeRepo


class UOWFirmware(IUOWFirmware, UOW):
    def __init__(self, sql_session: AsyncSession, s3_session: Minio) -> None:
        self.sql_session = sql_session
        self.s3_session = s3_session

        self.firm_s3_repo = get_firmware_s3_repo(self.s3_session)
        self.firm_sql_repo = get_firmware_info_repo(self.sql_session)
        self.type_repo = get_type_repo(self.sql_session)


def get_firmware_uow_service(
    s3_client: S3ClientType, sql_session: DBSessionType
) -> IUOWFirmware:
    return UOWFirmware(sql_session=sql_session, s3_session=s3_client)


FirmwareUOWType = Annotated[IUOWFirmware, Depends(get_firmware_uow_service)]
