from abc import ABC, abstractmethod
from typing import Annotated
from uuid import UUID

from calypte_api.common.exceptions import ObjectNotFoundError
from calypte_api.types.schemas import (
    CreateTypeRequestBody,
    CreateTypeResponse,
    GetTypeResponse,
    TypeFilter,
    UpdateTypeRequestBody,
    UpdateTypeResponse,
)
from calypte_api.types.uow import UOWTypeType

from fastapi import Depends
from fastapi_pagination import Page, Params


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
        self,
        company_id: UUID,
        pagination_params: Params,
        filtration_params: TypeFilter,
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
    def __init__(self, uow: UOWTypeType):
        self.uow = uow

    async def get_type(
        self,
        company_id: UUID,
        type_id: UUID,
    ) -> GetTypeResponse:
        type_schema = await self.uow.type_repo.get_type_by_id(
            company_id=company_id,
            type_id=type_id,
        )

        if not type_schema:
            raise ObjectNotFoundError(object_id=type_id)

        return type_schema

    async def get_types(
        self,
        company_id: UUID,
        pagination_params: Params,
        filtration_params: TypeFilter,
    ) -> Page[GetTypeResponse]:
        types = await self.uow.type_repo.get_types(
            company_id=company_id,
            pagination_params=pagination_params,
            filtration_params=filtration_params,
        )
        return types

    async def create_type(
        self, company_id: UUID, request_body: CreateTypeRequestBody
    ) -> CreateTypeResponse:
        async with self.uow as uow:
            created_type = await uow.type_repo.create_type(
                company_id=company_id,
                name=request_body.name,
                description=request_body.description,
            )
            await uow.commit()

        return created_type

    async def update_type(
        self,
        company_id: UUID,
        type_id: UUID,
        request_body: UpdateTypeRequestBody,
    ) -> UpdateTypeResponse:
        async with self.uow as uow:
            updated_type = await uow.type_repo.update_type(
                company_id=company_id,
                type_id=type_id,
                name=request_body.name,
                description=request_body.description,
            )
            await uow.commit()
        return updated_type

    async def delete_type(self, company_id: UUID, type_id: UUID) -> None:
        async with self.uow as uow:
            await uow.type_repo.delete_type(
                company_id=company_id,
                type_id=type_id,
            )
            await uow.commit()


def get_type_service(uow: UOWTypeType) -> ITypeService:
    return TypeService(uow=uow)


TypeServiceType = Annotated[ITypeService, Depends(get_type_service)]
