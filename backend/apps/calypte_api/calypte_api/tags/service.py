from abc import ABC, abstractmethod
from typing import Annotated
from uuid import UUID

from calypte_api.tags.repository import ITagRepo, RepositoryType
from calypte_api.tags.schemas import (
    CreateTagRequestBody,
    CreateTagResponse,
    GetTagQueryParams,
    GetTagResponse,
    UpdateTagRequestBody,
    UpdateTagResponse,
)

from fastapi import Depends
from fastapi_pagination import Page


class ITagService(ABC):
    @abstractmethod
    async def get_tag(
        self,
        user_id: UUID,
        tag_id: UUID,
    ) -> GetTagResponse:
        """
        Get tag by id

        Args:
            user_id (UUID): user id
            tag_id (UUID): tag id

        """

    @abstractmethod
    async def get_tags(
        self, user_id: UUID, query_params: GetTagQueryParams
    ) -> Page[GetTagResponse]:
        """
        Get all tags

        Args:
            user_id (UUID): user id

        """

    @abstractmethod
    async def create_tag(
        self, user_id: UUID, request_body: CreateTagRequestBody
    ) -> CreateTagResponse:
        """
        Create tag

        Args:
            user_id (UUID): user id
            request_body (CreateTagRequestBody): request body

        """

    @abstractmethod
    async def update_tag(
        self,
        user_id: UUID,
        tag_id: UUID,
        request_body: UpdateTagRequestBody,
    ) -> UpdateTagResponse:
        """
        Update tag

        Args:
            user_id (UUID): user id
            tag_id (UUID): tag id
            request_body (CreateTagRequestBody): request body
        """

    @abstractmethod
    async def delete_tag(self, user_id: UUID, tag_id: UUID) -> None:
        """
        Delete tag

        Args:
            user_id (UUID): user id
            tag_id (UUID): tag id
        """


class TagService(ITagService):
    def __init__(self, tag_repo: ITagRepo):
        self.tag_repo = tag_repo

    async def get_tag(
        self,
        user_id: UUID,
        tag_id: UUID,
    ) -> GetTagResponse:
        return await self.tag_repo.get_tag_by_id(
            user_id=user_id,
            tag_id=tag_id,
        )

    async def get_tags(
        self, user_id: UUID, query_params: GetTagQueryParams
    ) -> Page[GetTagResponse]:
        tags = await self.tag_repo.get_tags(
            user_id=user_id,
            query_params=query_params,
        )
        return Page.create(
            items=tags,
            params=query_params,
            total=query_params.size,
        )

    async def create_tag(
        self, user_id: UUID, request_body: CreateTagRequestBody
    ) -> CreateTagResponse:
        return await self.tag_repo.create_tag(
            user_id=user_id,
            name=request_body.name,
        )

    async def update_tag(
        self,
        user_id: UUID,
        tag_id: UUID,
        request_body: UpdateTagRequestBody,
    ) -> UpdateTagResponse:
        return await self.tag_repo.update_tag(
            user_id=user_id,
            tag_id=tag_id,
            name=request_body.name,
        )

    async def delete_tag(self, user_id: UUID, tag_id: UUID) -> None:
        return await self.tag_repo.delete_tag(user_id=user_id, tag_id=tag_id)


def get_tag_service(tag_repo: RepositoryType) -> ITagService:
    return TagService(tag_repo=tag_repo)


TagServiceType = Annotated[ITagService, Depends(get_tag_service)]
