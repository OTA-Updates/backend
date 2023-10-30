from abc import ABC, abstractmethod
from typing import Annotated
from uuid import UUID

from calypte_api.types.repository import ITypeRepo, TypeRepositoryType
from calypte_api.types.schemas import (
    CreateTypeRequestBody,
    CreateTypeResponse,
    GetTypeQueryParams,
    GetTypeResponse,
    UpdateTypeRequestBody,
    UpdateTypeResponse,
)

from fastapi import Depends
from fastapi_pagination import Page


class ITypeService(ABC):
    @abstractmethod
    async def get_type(
        self,
        user_id: UUID,
        type_id: UUID,
    ) -> GetTypeResponse:
        """
        Get type by id

        Args:
            user_id (UUID): user id
            type_id (UUID): type id

        """

    @abstractmethod
    async def get_types(
        self, user_id: UUID, query_params: GetTypeQueryParams
    ) -> Page[GetTypeResponse]:
        """
        Get all types

        Args:
            user_id (UUID): user id
            query_params (GetTypeQueryParams): query params

        """

    @abstractmethod
    async def create_type(
        self, user_id: UUID, request_body: CreateTypeRequestBody
    ) -> CreateTypeResponse:
        """
        Create type

        Args:
            user_id (UUID): user id
            request_body (CreateTypeRequestBody): request body

        """

    @abstractmethod
    async def update_type(
        self,
        user_id: UUID,
        type_id: UUID,
        request_body: UpdateTypeRequestBody,
    ) -> UpdateTypeResponse:
        """
        Update type

        Args:
            user_id (UUID): user id
            type_id (UUID): type id
            request_body (CreateTypeRequestBody): request body
        """

    @abstractmethod
    async def delete_type(self, user_id: UUID, type_id: UUID) -> None:
        """
        Delete type

        Args:
            user_id (UUID): user id
            type_id (UUID): type id
        """


class TypeService(ITypeService):
    def __init__(self, type_repo: ITypeRepo):
        self.type_repo = type_repo

    async def get_type(
        self,
        user_id: UUID,
        type_id: UUID,
    ) -> GetTypeResponse:
        return await self.type_repo.get_type_by_id(
            user_id=user_id,
            type_id=type_id,
        )

    async def get_types(
        self, user_id: UUID, query_params: GetTypeQueryParams
    ) -> Page[GetTypeResponse]:
        types = await self.type_repo.get_types(
            user_id=user_id, query_params=query_params
        )
        return Page.create(
            items=types,
            params=query_params,
            total=query_params.size,
        )

    async def create_type(
        self, user_id: UUID, request_body: CreateTypeRequestBody
    ) -> CreateTypeResponse:
        return await self.type_repo.create_type(
            user_id=user_id,
            name=request_body.name,
            description=request_body.description,
        )

    async def update_type(
        self,
        user_id: UUID,
        type_id: UUID,
        request_body: UpdateTypeRequestBody,
    ) -> UpdateTypeResponse:
        return await self.type_repo.update_type(
            user_id=user_id,
            type_id=type_id,
            name=request_body.name,
            description=request_body.description,
        )

    async def delete_type(self, user_id: UUID, type_id: UUID) -> None:
        return await self.type_repo.delete_type(user_id=user_id, type_id=type_id)


def get_type_service(type_repo: TypeRepositoryType) -> ITypeService:
    return TypeService(type_repo=type_repo)


TypeServiceType = Annotated[ITypeService, Depends(get_type_service)]
