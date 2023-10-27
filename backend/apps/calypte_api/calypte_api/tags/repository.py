from abc import ABC, abstractmethod
from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from calypte_api.common.dependencies import DBSessionType
from calypte_api.tags.schemas import (
    CreateTagResponse,
    GetTagQueryParams,
    GetTagResponse,
    UpdateTagResponse,
)

from fastapi import Depends
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
        self, user_id: UUID, query_params: GetTagQueryParams
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
        name: str,
        user_id: UUID,
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
        self, user_id: UUID, tag_id: UUID, name: str
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


class TagRepo(ITagRepo):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    # TODO: implement
    async def get_tag_by_id(
        self,
        user_id: UUID,
        tag_id: UUID,
    ) -> GetTagResponse:
        return GetTagResponse(
            id=tag_id,
            name="mocked tag name",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    # TODO: implement
    async def get_tags(
        self, user_id: UUID, query_params: GetTagQueryParams
    ) -> list[GetTagResponse]:
        return [
            GetTagResponse(
                id=uuid4(),
                name="mocked tag name 1",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            for i in range(query_params.size)
        ]

    # TODO: implement
    async def create_tag(
        self,
        user_id: UUID,
        name: str,
    ) -> CreateTagResponse:
        return CreateTagResponse(
            id=uuid4(),
            name=name,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    # TODO: implement
    async def update_tag(
        self, user_id: UUID, tag_id: UUID, name: str
    ) -> UpdateTagResponse:
        return UpdateTagResponse(
            id=tag_id,
            name=name,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    # TODO: implement
    async def delete_tag(self, user_id: UUID, tag_id: UUID) -> None:
        return None


def get_tag_repo(db_session: DBSessionType) -> ITagRepo:
    return TagRepo(db_session=db_session)


TagRepositoryType = Annotated[ITagRepo, Depends(get_tag_repo)]
