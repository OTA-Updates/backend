from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession


class IUOW(ABC):
    @abstractmethod
    async def __aenter__(self) -> Self:
        ...

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[Exception],
        exc_val: Exception,
        exc_tb: TracebackType,
    ):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UOW(IUOW):
    def __init__(self, sql_session: AsyncSession) -> None:
        self.sql_session = sql_session

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
