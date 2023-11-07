from uuid import UUID

from calypte_api.common.exceptions import ObjectNotFoundError
from calypte_api.types.repositories import ITypeRepo


async def validate_type_id(
    type_repo: ITypeRepo, type_id: UUID, company_id: UUID
) -> None:
    result = await type_repo.check_type_belongs_to_company(
        company_id=company_id, type_id=type_id
    )

    if not result:
        raise ObjectNotFoundError(object_id=type_id)
