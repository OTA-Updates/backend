from abc import ABC, abstractmethod
from typing import Annotated
from uuid import UUID

from calypte_api.common.dependencies import DBSessionType
from calypte_api.tags.models import Tag
from calypte_api.tags.schemas import (
    CreateTagResponse,
    GetTagResponse,
    UpdateTagResponse,
)

from fastapi import Depends
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class ITagRepo(ABC):
    @abstractmethod
    async def get_tag_by_id(
        self,
        user_id: UUID,
        tag_id: UUID,
    ) -> GetTagResponse:
        """
        Get tag by id

        Args:
            tag_id (UUID): tag id
            user_id (UUID): user id

        """

    @abstractmethod
    async def get_tags(
        self, user_id: UUID, limit: int, offset: int, name: str | None
    ) -> list[GetTagResponse]:
        """
        Get tags by query params

        Args:
            user_id (UUID): user id
            query_params (GetTagQueryParams): query params
        """

    @abstractmethod
    async def create_tag(
        self,
        company_id: UUID,
        type_id: UUID,
        color: str,
        name: str,
    ) -> CreateTagResponse:
        """
        Create tag

        Args:
            user_id (UUID): user id
            name (str): tag name
            tags (list[UUID]): tag tags
        """

    @abstractmethod
    async def update_tag(
        self,
        company_id: UUID,
        tag_id: UUID,
        color: str,
        name: str,
    ) -> UpdateTagResponse:
        """
        Update tag

        Args:
            user_id (UUID): user id
            tag_id (UUID): tag id
            name (str): tag name
            tags (list[UUID]): tag tags
        """

    @abstractmethod
    async def delete_tag(self, user_id: UUID, tag_id: UUID) -> None:
        """
        Delete tag

        Args:
            user_id (UUID): user id
            tag_id (UUID): tag id
        """

    @abstractmethod
    async def check_tags_belongs_to(
        self,
        tags: list[UUID],
        company_id: UUID | None = None,
        type_id: UUID | None = None,
    ) -> None:
        """
        Check tags belongs to company or type

        Args:
            tags (list[UUID]): tags
            company_id (UUID): company id
            type_id (UUID): type id
        """


class TagRepo(ITagRepo):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def get_tag_by_id(
        self,
        company_id: UUID,
        tag_id: UUID,
    ) -> GetTagResponse | None:
        select_stmt = (
            select(Tag)
            .where(Tag.id == tag_id)
            .where(Tag.company_id == company_id)
        )
        tag_model = await self.db_session.scalar(select_stmt)

        if not tag_model:
            return None

        return GetTagResponse.model_validate(tag_model)

    async def get_tags(
        self,
        company_id: UUID,
        limit: int,
        offset: int,
        type_id: UUID | None,
        name: str | None,
    ) -> list[GetTagResponse]:
        select_stmt = select(Tag).where(Tag.company_id == company_id)
        if name:
            select_stmt = select_stmt.where(Tag.name == name)
        if type_id:
            select_stmt = select_stmt.where(Tag.type_id == type_id)

        select_stmt = (
            select_stmt.limit(limit).offset(offset).order_by(Tag.created_at)
        )
        tags_models = await self.db_session.scalars(select_stmt)

        tag_schemas = [
            GetTagResponse.model_validate(tag_model)
            for tag_model in tags_models
        ]
        return tag_schemas

    async def create_tag(
        self,
        company_id: UUID,
        type_id: UUID,
        color: str,
        name: str,
    ) -> CreateTagResponse:
        insert_stmt = (
            insert(Tag)
            .values(
                company_id=company_id,
                type_id=type_id,
                name=name,
            )
            .returning(Tag)
        )
        tag_model = await self.db_session.scalar(insert_stmt)
        return CreateTagResponse.model_validate(tag_model)

    async def update_tag(
        self,
        company_id: UUID,
        tag_id: UUID,
        color: str,
        name: str,
    ) -> UpdateTagResponse:
        update_stmt = (
            update(Tag)
            .where(Tag.id == tag_id)
            .where(Tag.company_id == company_id)
            .values(name=name, color=color)
            .returning(Tag)
        )

        tag_model = await self.db_session.scalar(update_stmt)
        return UpdateTagResponse.model_validate(tag_model)

    async def delete_tag(self, company_id: UUID, tag_id: UUID) -> None:
        delete_stmt = (
            delete(Tag)
            .where(Tag.id == tag_id)
            .where(Tag.company_id == company_id)
        )
        await self.db_session.execute(delete_stmt)

    async def check_tags_belongs_to(
        self,
        tags: list[UUID],
        company_id: UUID | None = None,
        type_id: UUID | None = None,
    ) -> bool:
        select_stmt = select(Tag).where(Tag.id.in_(tags))
        if company_id:
            select_stmt = select_stmt.where(Tag.company_id == company_id)
        if type_id:
            select_stmt = select_stmt.where(Tag.type_id == type_id)

        tags_models = await self.db_session.scalars(select_stmt)

        return len(tags_models.all()) == len(tags)


def get_tag_repo(db_session: DBSessionType) -> ITagRepo:
    return TagRepo(db_session=db_session)


TagRepositoryType = Annotated[ITagRepo, Depends(get_tag_repo)]
