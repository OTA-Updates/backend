from abc import ABC, abstractmethod
from typing import Annotated
from uuid import UUID

from calypte_api.common.exceptions import ObjectNotFoundError
from calypte_api.groups.schemas import (
    CreateGroupRequestBody,
    CreateGroupResponse,
    GetGroupResponse,
    GroupFilter,
    UpdateGroupRequestBody,
    UpdateGroupResponse,
)
from calypte_api.groups.uow import IUOWGroups, UOWGroupType
from calypte_api.types.validators import validate_type_id

from fastapi import Depends
from fastapi_pagination import Page, Params


class IGroupService(ABC):
    @abstractmethod
    async def get_group(
        self,
        company_id: UUID,
        group_id: UUID,
    ) -> GetGroupResponse:
        """
        Get group by id

        Args:
            company_id (UUID): user id
            group_id (UUID): group id

        """

    @abstractmethod
    async def get_groups(
        self,
        company_id: UUID,
        pagination_params: Params,
        filtration_params: GroupFilter,
    ) -> Page[GetGroupResponse]:
        """
        Get all groups

        Args:
            company_id (UUID): user id

        """

    @abstractmethod
    async def create_group(
        self, company_id: UUID, request_body: CreateGroupRequestBody
    ) -> CreateGroupResponse:
        """
        Create group

        Args:
            company_id (UUID): user id
            request_body (CreateGroupRequestBody): request body

        """

    @abstractmethod
    async def update_group(
        self,
        company_id: UUID,
        group_id: UUID,
        request_body: UpdateGroupRequestBody,
    ) -> UpdateGroupResponse:
        """
        Update group

        Args:
            company_id (UUID): user id
            group_id (UUID): group id
            request_body (CreateGroupRequestBody): request body
        """

    @abstractmethod
    async def delete_group(self, company_id: UUID, group_id: UUID) -> None:
        """
        Delete group

        Args:
            company_id (UUID): user id
            group_id (UUID): group id
        """


class GroupService(IGroupService):
    def __init__(self, uow: IUOWGroups):
        self.uow = uow

    async def get_group(
        self, company_id: UUID, group_id: UUID
    ) -> GetGroupResponse:
        group_schema = await self.uow.group_repo.get_group_by_id(
            company_id=company_id,
            group_id=group_id,
        )

        if not group_schema:
            raise ObjectNotFoundError(object_id=group_id)

        return group_schema

    async def get_groups(
        self,
        company_id: UUID,
        pagination_params: Params,
        filtration_params: GroupFilter,
    ) -> Page[GetGroupResponse]:
        groups = await self.uow.group_repo.get_groups(
            company_id=company_id,
            pagination_params=pagination_params,
            filtration_params=filtration_params,
        )
        return groups

    async def create_group(
        self, company_id: UUID, request_body: CreateGroupRequestBody
    ) -> CreateGroupResponse:
        async with self.uow as uow:
            await validate_type_id(
                type_repo=uow.type_repo,
                type_id=request_body.type_id,
                company_id=company_id,
            )

            group_schema = await uow.group_repo.create_group(
                company_id=company_id,
                name=request_body.name,
                type_id=request_body.type_id,
            )
            await uow.commit()

            return group_schema

    async def update_group(
        self,
        company_id: UUID,
        group_id: UUID,
        request_body: UpdateGroupRequestBody,
    ) -> UpdateGroupResponse:
        async with self.uow as uow:
            group_schema = await uow.group_repo.update_group(
                company_id=company_id,
                group_id=group_id,
                name=request_body.name,
            )
            await uow.commit()
            return group_schema

    async def delete_group(self, company_id: UUID, group_id: UUID) -> None:
        async with self.uow as uow:
            await self.uow.group_repo.delete_group(
                company_id=company_id, group_id=group_id
            )
            await uow.commit()


def get_group_service(uow: UOWGroupType) -> IGroupService:
    return GroupService(uow=uow)


GroupServiceType = Annotated[IGroupService, Depends(get_group_service)]
