from uuid import UUID

from calypte_api.common.exceptions import ObjectNotFoundError
from calypte_api.groups.repositories import IGroupRepo


async def validate_group_id(
    group_repo: IGroupRepo, group_id: UUID, company_id: UUID, type_id: UUID
) -> None:
    result = await group_repo.check_groups_belongs_to(
        group_id=group_id, company_id=company_id, type_id=type_id
    )

    if not result:
        raise ObjectNotFoundError(object_id=group_id)
