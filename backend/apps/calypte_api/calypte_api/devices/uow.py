from typing import Annotated

from calypte_api.common.dependencies import DBSessionType
from calypte_api.common.uow import IUOW, UOW
from calypte_api.devices.repositories import IDeviceRepo, get_device_repo
from calypte_api.firmware.repositories import (
    IFirmwareInfoRepo,
    get_firmware_info_repo,
)
from calypte_api.groups.repositories import IGroupRepo, get_group_repo
from calypte_api.types.repositories import ITypeRepo, get_type_repo

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


class IUOWDevices(IUOW):
    device_repo: IDeviceRepo
    type_repo: ITypeRepo
    group_repo: IGroupRepo
    firmware_repo: IFirmwareInfoRepo


class UOWDevice(IUOWDevices, UOW):
    def __init__(self, sql_session: AsyncSession) -> None:
        self.sql_session = sql_session

        self.device_repo = get_device_repo(self.sql_session)
        self.type_repo = get_type_repo(self.sql_session)
        self.group_repo = get_group_repo(self.sql_session)
        self.firmware_repo = get_firmware_info_repo(self.sql_session)


def get_device_uow_service(sql_session: DBSessionType) -> IUOWDevices:
    return UOWDevice(sql_session=sql_session)


UOWDeviceType = Annotated[IUOWDevices, Depends(get_device_uow_service)]
