from abc import ABC, abstractmethod
from collections.abc import Sequence
from uuid import UUID

from calypte_api.groups.models import Group
from calypte_api.groups.schemas import (
    CreateGroupResponse,
    GetGroupResponse,
    GroupFilter,
    UpdateGroupResponse,
)

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class IGroupRepo(ABC):
    @abstractmethod
    async def get_group_by_id(
        self,
        company_id: UUID,
        group_id: UUID,
    ) -> GetGroupResponse | None:
        """
        Get group by id

        Args:
            group_id (UUID): group id
            company_id (UUID): user id

        """

    @abstractmethod
    async def get_groups(
        self,
        company_id: UUID,
        pagination_params: Params,
        filtration_params: GroupFilter,
    ) -> Page[GetGroupResponse]:
        """
        Get groups by query params

        Args:
            company_id (UUID): user id
            query_params (GetGroupQueryParams): query params
        """

    @abstractmethod
    async def create_group(
        self,
        company_id: UUID,
        type_id: UUID,
        name: str,
    ) -> CreateGroupResponse:
        """
        Create group

        Args:
            company_id (UUID): user id
            type_id (UUID): type id
            assigned_firmware_id (str): assigned firmware id
            name (str): group name
        """

    @abstractmethod
    async def update_group(
        self,
        company_id: UUID,
        group_id: UUID,
        name: str,
    ) -> UpdateGroupResponse:
        """
        Update group

        Args:
            company_id (UUID): user id
            group_id (UUID): group id
            name (str): group name
        """

    @abstractmethod
    async def delete_group(self, company_id: UUID, group_id: UUID) -> None:
        """
        Delete group

        Args:
            company_id (UUID): user id
            group_id (UUID): group id
        """

    @abstractmethod
    async def check_groups_belongs_to(
        self,
        group_id: UUID,
        company_id: UUID | None = None,
        type_id: UUID | None = None,
    ) -> bool:
        """
        Check groups belongs to company or type

        Args:
            groups (list[UUID]): groups
            company_id (UUID): company id
            type_id (UUID): type id
        """


class GroupRepo(IGroupRepo):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def get_group_by_id(
        self,
        company_id: UUID,
        group_id: UUID,
    ) -> GetGroupResponse | None:
        select_stmt = (
            select(Group)
            .where(Group.id == group_id)
            .where(Group.company_id == company_id)
        )
        group_model = await self.db_session.scalar(select_stmt)

        if not group_model:
            return None

        return GetGroupResponse.model_validate(group_model)

    async def _transformer(
        self, models: Sequence[Group]
    ) -> list[GetGroupResponse]:
        return [GetGroupResponse.model_validate(model) for model in models]

    async def get_groups(
        self,
        company_id: UUID,
        pagination_params: Params,
        filtration_params: GroupFilter,
    ) -> Page[GetGroupResponse]:
        select_stmt = select(Group).where(Group.company_id == company_id)

        select_stmt = filtration_params.filter(select_stmt)
        select_stmt = filtration_params.sort(select_stmt)

        group_schemas = await paginate(
            self.db_session,
            select_stmt,
            params=pagination_params,
            transformer=self._transformer,
        )
        return group_schemas

    async def create_group(
        self,
        company_id: UUID,
        type_id: UUID,
        name: str,
    ) -> CreateGroupResponse:
        insert_stmt = (
            insert(Group)
            .values(
                company_id=company_id,
                type_id=type_id,
                name=name,
            )
            .returning(Group)
        )
        group_model = await self.db_session.scalar(insert_stmt)

        return CreateGroupResponse.model_validate(group_model)

    async def update_group(
        self,
        company_id: UUID,
        group_id: UUID,
        name: str,
    ) -> UpdateGroupResponse:
        update_stmt = (
            update(Group)
            .where(Group.id == group_id)
            .where(Group.company_id == company_id)
            .values(name=name)
            .returning(Group)
        )

        group_model = await self.db_session.scalar(update_stmt)

        return UpdateGroupResponse.model_validate(group_model)

    async def delete_group(self, company_id: UUID, group_id: UUID) -> None:
        delete_stmt = (
            delete(Group)
            .where(Group.id == group_id)
            .where(Group.company_id == company_id)
        )
        await self.db_session.execute(delete_stmt)

    async def check_groups_belongs_to(
        self,
        group_id: UUID,
        company_id: UUID | None = None,
        type_id: UUID | None = None,
    ) -> bool:
        # TODO: optimize query
        select_stmt = select(Group).where(Group.id == group_id)
        if company_id:
            select_stmt = select_stmt.where(Group.company_id == company_id)
        if type_id:
            select_stmt = select_stmt.where(Group.type_id == type_id)

        group_model = await self.db_session.scalar(select_stmt)

        return bool(group_model)


def get_group_repo(db_session: AsyncSession) -> IGroupRepo:
    return GroupRepo(db_session=db_session)
