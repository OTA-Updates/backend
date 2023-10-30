from abc import ABC, abstractmethod
from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from calypte_api.common.dependencies import DBSessionType
from calypte_api.types.schemas import (
    CreateTypeResponse,
    GetTypeQueryParams,
    GetTypeResponse,
    UpdateTypeResponse,
)

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


class ITypeRepo(ABC):
    @abstractmethod
    async def get_type_by_id(
        self,
        user_id: UUID,
        type_id: UUID,
    ) -> GetTypeResponse:
        """
        Get type by id

        Args:
            type_id (UUID): type id
            user_id (UUID): user id

        """

    @abstractmethod
    async def get_types(
        self, user_id: UUID, query_params: GetTypeQueryParams
    ) -> list[GetTypeResponse]:
        """
        Get types by query params

        Args:
            user_id (UUID): user id
            query_params (GetTypeQueryParams): query params
        """

    @abstractmethod
    async def create_type(
        self,
        user_id: UUID,
        name: str,
        description: str | None,
    ) -> CreateTypeResponse:
        """
        Create type

        Args:
            user_id (UUID): user id
            name (str): type name
            description (str | None): type description
        """

    @abstractmethod
    async def update_type(
        self, user_id: UUID, type_id: UUID, name: str, description: str | None
    ) -> UpdateTypeResponse:
        """
        Update type

        Args:
            user_id (UUID): user id
            type_id (UUID): type id
            name (str): type name
            description (str | None): type description
        """

    @abstractmethod
    async def delete_type(self, user_id: UUID, type_id: UUID) -> None:
        """
        Delete type

        Args:
            user_id (UUID): user id
            type_id (UUID): type id
        """


class TypeRepo(ITypeRepo):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    # TODO: implement
    async def get_type_by_id(
        self,
        user_id: UUID,
        type_id: UUID,
    ) -> GetTypeResponse:
        return GetTypeResponse(
            id=type_id,
            name="type name",
            description="type description",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    # TODO: implement
    async def get_types(
        self, user_id: UUID, query_params: GetTypeQueryParams
    ) -> list[GetTypeResponse]:
        return [
            GetTypeResponse(
                id=uuid4(),
                name="type name",
                description="type description",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            for _ in range(query_params.size)
        ]

    # TODO: implement
    async def create_type(
        self,
        user_id: UUID,
        name: str,
        description: str | None,
    ) -> CreateTypeResponse:
        return CreateTypeResponse(
            id=uuid4(),
            name=name,
            description=description,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    # TODO: implement
    async def update_type(
        self,
        user_id: UUID,
        type_id: UUID,
        name: str,
        description: str | None,
    ) -> UpdateTypeResponse:
        return UpdateTypeResponse(
            id=type_id,
            name=name,
            description=description,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    # TODO: implement
    async def delete_type(self, user_id: UUID, type_id: UUID) -> None:
        return None


def get_type_repo(db_session: DBSessionType) -> ITypeRepo:
    return TypeRepo(db_session=db_session)


TypeRepositoryType = Annotated[ITypeRepo, Depends(get_type_repo)]
