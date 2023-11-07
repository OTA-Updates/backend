from typing import Annotated

from calypte_api.common.dependencies import DBSessionType
from calypte_api.common.uow import IUOW, UOW
from calypte_api.groups.repositories import IGroupRepo, get_group_repo
from calypte_api.types.repositories import ITypeRepo, get_type_repo

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


class IUOWGroups(IUOW):
    type_repo: ITypeRepo
    group_repo: IGroupRepo


class UOWGroup(IUOWGroups, UOW):
    def __init__(self, sql_session: AsyncSession) -> None:
        self.sql_session = sql_session
        self.type_repo = get_type_repo(self.sql_session)
        self.group_repo = get_group_repo(self.sql_session)


def get_group_uow_service(sql_session: DBSessionType) -> IUOWGroups:
    return UOWGroup(sql_session=sql_session)


UOWGroupType = Annotated[IUOWGroups, Depends(get_group_uow_service)]
