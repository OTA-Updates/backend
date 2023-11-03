from abc import ABC, abstractmethod
from typing import Annotated
from uuid import UUID

from calypte_api.common.exeptions import ObjectNotFoundError
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
        company_id: UUID,
        type_id: UUID,
    ) -> GetTypeResponse:
        """
        Get type by id

        Args:
            company_id (UUID): user id
            type_id (UUID): type id

        """

    @abstractmethod
    async def get_types(
        self, company_id: UUID, query_params: GetTypeQueryParams
    ) -> Page[GetTypeResponse]:
        """
        Get all types

        Args:
            company_id (UUID): user id
            query_params (GetTypeQueryParams): query params

        """

    @abstractmethod
    async def create_type(
        self, company_id: UUID, request_body: CreateTypeRequestBody
    ) -> CreateTypeResponse:
        """
        Create type

        Args:
            company_id (UUID): user id
            request_body (CreateTypeRequestBody): request body

        """

    @abstractmethod
    async def update_type(
        self,
        company_id: UUID,
        type_id: UUID,
        request_body: UpdateTypeRequestBody,
    ) -> UpdateTypeResponse:
        """
        Update type

        Args:
            company_id (UUID): user id
            type_id (UUID): type id
            request_body (CreateTypeRequestBody): request body
        """

    @abstractmethod
    async def delete_type(self, company_id: UUID, type_id: UUID) -> None:
        """
        Delete type

        Args:
            company_id (UUID): user id
            type_id (UUID): type id
        """


class TypeService(ITypeService):
    def __init__(self, type_repo: ITypeRepo):
        self.type_repo = type_repo

    async def get_type(
        self,
        company_id: UUID,
        type_id: UUID,
    ) -> GetTypeResponse:
        type_schema = await self.type_repo.get_type_by_id(
            company_id=company_id,
            type_id=type_id,
        )

        if not type_schema:
            raise ObjectNotFoundError(object_id=type_id)

        return type_schema

    async def get_types(
        self, company_id: UUID, query_params: GetTypeQueryParams
    ) -> Page[GetTypeResponse]:
        limit = query_params.size
        offset = (query_params.page - 1) * query_params.size

        types = await self.type_repo.get_types(
            company_id=company_id,
            name=query_params.name,
            limit=limit,
            offset=offset,
        )
        return Page.create(
            items=types,
            params=query_params,
            total=query_params.size,
        )

    async def create_type(
        self, company_id: UUID, request_body: CreateTypeRequestBody
    ) -> CreateTypeResponse:
        return await self.type_repo.create_type(
            company_id=company_id,
            name=request_body.name,
            description=request_body.description,
        )

    async def update_type(
        self,
        company_id: UUID,
        type_id: UUID,
        request_body: UpdateTypeRequestBody,
    ) -> UpdateTypeResponse:
        return await self.type_repo.update_type(
            company_id=company_id,
            type_id=type_id,
            name=request_body.name,
            description=request_body.description,
        )

    async def delete_type(self, company_id: UUID, type_id: UUID) -> None:
        return await self.type_repo.delete_type(
            company_id=company_id,
            type_id=type_id,
        )


def get_type_service(type_repo: TypeRepositoryType) -> ITypeService:
    return TypeService(type_repo=type_repo)


TypeServiceType = Annotated[ITypeService, Depends(get_type_service)]
