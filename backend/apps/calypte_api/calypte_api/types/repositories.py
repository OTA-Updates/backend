from abc import ABC, abstractmethod
from collections.abc import Sequence
from uuid import UUID

from calypte_api.types.models import Type
from calypte_api.types.schemas import (
    CreateTypeResponse,
    GetTypeResponse,
    TypeFilter,
    UpdateTypeResponse,
)

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class ITypeRepo(ABC):
    @abstractmethod
    async def get_type_by_id(
        self,
        company_id: UUID,
        type_id: UUID,
    ) -> GetTypeResponse | None:
        """
        Get type by id

        Args:
            type_id (UUID): type id
            company_id (UUID): user id

        """

    @abstractmethod
    async def get_types(
        self,
        company_id: UUID,
        pagination_params: Params,
        filtration_params: TypeFilter,
    ) -> Page[GetTypeResponse]:
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
    ) -> bool:
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

        if types_models is None:
            return None

        return GetTypeResponse.model_validate(types_models)

    def _transformer(self, models: Sequence[Type]) -> list[GetTypeResponse]:
        return [GetTypeResponse.model_validate(model) for model in models]

    async def get_types(
        self,
        company_id: UUID,
        pagination_params: Params,
        filtration_params: TypeFilter,
    ) -> Page[GetTypeResponse]:
        select_stmt = select(Type).where(Type.company_id == company_id)
        select_stmt = filtration_params.filter(select_stmt)
        select_stmt = filtration_params.sort(select_stmt)

        get_type_schemas = await paginate(
            self.db_session,
            select_stmt,
            params=pagination_params,
            transformer=self._transformer,
        )

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


def get_type_repo(db_session: AsyncSession) -> ITypeRepo:
    return TypeRepo(db_session=db_session)
