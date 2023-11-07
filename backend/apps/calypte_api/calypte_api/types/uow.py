from typing import Annotated

from calypte_api.common.dependencies import DBSessionType
from calypte_api.common.uow import IUOW, UOW
from calypte_api.types.repositories import ITypeRepo, get_type_repo

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


class IUOWTypes(IUOW):
    type_repo: ITypeRepo


class UOWType(IUOWTypes, UOW):
    def __init__(self, sql_session: AsyncSession) -> None:
        self.sql_session = sql_session
        self.type_repo = get_type_repo(self.sql_session)


def get_type_uow_service(sql_session: DBSessionType) -> IUOWTypes:
    return UOWType(sql_session=sql_session)


UOWTypeType = Annotated[IUOWTypes, Depends(get_type_uow_service)]
