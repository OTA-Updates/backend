from abc import ABC, abstractmethod
from typing import Generic, TypeVar


ResponseType = TypeVar("ResponseType")


class ICommand(ABC, Generic[ResponseType]):
    @abstractmethod
    async def execute(self) -> ResponseType:
        ...

    @abstractmethod
    async def rollback(self):
        ...
