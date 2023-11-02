from abc import ABC, abstractmethod
from typing import Annotated
from uuid import UUID

from calypte_api.common.dependencies import DBSessionType
from calypte_api.types.models import Type
from calypte_api.types.schemas import (
    CreateTypeResponse,
    GetTypeResponse,
    UpdateTypeResponse,
)

from fastapi import Depends
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class ITypeRepo(ABC):
    @abstractmethod
    async def get_type_by_id(
        self,
        company_id: UUID,
        type_id: UUID,
    ) -> GetTypeResponse:
        """
        Get type by id

        Args:
            type_id (UUID): type id
            company_id (UUID): user id

        """

    @abstractmethod
    async def get_types(
        self, company_id: UUID, name: str | None, offset: int, limit: int
    ) -> list[GetTypeResponse]:
        """
        Get types by query params

        Args:
            company_id (UUID): user id
            query_params (GetTypeQueryParams): query params
        """

    @abstractmethod
    async def create_type(
        self,
        company_id: UUID,
        name: str,
        description: str | None,
    ) -> CreateTypeResponse:
        """
        Create type

        Args:
            company_id (UUID): user id
            name (str): type name
            description (str | None): type description
        """

    @abstractmethod
    async def update_type(
        self,
        company_id: UUID,
        type_id: UUID,
        name: str,
        description: str | None,
    ) -> UpdateTypeResponse:
        """
        Update type

        Args:
            company_id (UUID): user id
            type_id (UUID): type id
            name (str): type name
            description (str | None): type description
        """

    @abstractmethod
    async def delete_type(self, company_id: UUID, type_id: UUID) -> None:
        """
        Delete type

        Args:
            company_id (UUID): user id
            type_id (UUID): type id
        """

    @abstractmethod
    async def check_type_belongs_to_company(
        self, company_id: UUID, type_id: UUID
    ):
        """
        Check that type belongs to company

        Args:
            company_id (UUID): user id
            type_id (UUID): type id
        """


class TypeRepo(ITypeRepo):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def get_type_by_id(
        self,
        company_id: UUID,
        type_id: UUID,
    ) -> GetTypeResponse | None:
        select_stmt = (
            select(Type)
            .where(Type.company_id == company_id)
            .where(Type.id == type_id)
        )
        types_models = await self.db_session.scalar(statement=select_stmt)

        return types_models and GetTypeResponse.model_validate(types_models)

    async def get_types(
        self, company_id: UUID, name: str | None, offset: int, limit: int
    ) -> list[GetTypeResponse]:
        select_stmt = (
            select(Type)
            .where(Type.company_id == company_id)
            .order_by(Type.created_at)
            .offset(offset=offset)
            .limit(limit=limit)
        )
        if name is not None:
            select_stmt = select_stmt.where(Type.name == name)

        types_models = await self.db_session.scalars(statement=select_stmt)

        get_type_schemas = [
            GetTypeResponse.model_validate(type_model)
            for type_model in types_models
        ]
        return get_type_schemas

    async def create_type(
        self,
        company_id: UUID,
        name: str,
        description: str | None,
    ) -> CreateTypeResponse:
        insert_stmt = (
            insert(Type)
            .values(
                {
                    Type.name: name,
                    Type.description: description,
                    Type.company_id: company_id,
                }
            )
            .returning(Type)
        )
        result = await self.db_session.execute(insert_stmt)
        new_type = result.scalar_one()

        # * I am not sure commit about the commit in the repo
        # * It maybe make more sense to do it on higher level
        # await self.db_session.commit()

        return CreateTypeResponse.model_validate(new_type)

    async def update_type(
        self,
        company_id: UUID,
        type_id: UUID,
        name: str,
        description: str | None,
    ) -> UpdateTypeResponse:
        update_stmt = (
            update(Type)
            .where(Type.id == type_id)
            .where(Type.company_id == company_id)
            .values(name=name, description=description)
            .returning(Type)
        )
        result = await self.db_session.execute(update_stmt)
        new_type = result.scalar_one()

        return UpdateTypeResponse.model_validate(new_type)

    async def delete_type(self, company_id: UUID, type_id: UUID) -> None:
        delete_stmt = (
            delete(Type)
            .where(Type.id == type_id)
            .where(Type.company_id == company_id)
        )
        await self.db_session.execute(delete_stmt)

    async def check_type_belongs_to_company(
        self, company_id: UUID, type_id: UUID
    ) -> bool:
        # TODO: it make sense to optimize this query
        type_schema = await self.get_type_by_id(
            company_id=company_id, type_id=type_id
        )
        return bool(type_schema)


def get_type_repo(db_session: DBSessionType) -> ITypeRepo:
    return TypeRepo(db_session=db_session)


TypeRepositoryType = Annotated[ITypeRepo, Depends(get_type_repo)]
