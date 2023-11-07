from uuid import UUID

from calypte_api.common.exceptions import ObjectNotFoundError
from calypte_api.firmware.repositories import IFirmwareInfoRepo


async def validate_firmware_id(
    firmware_repo: IFirmwareInfoRepo,
    firmware_id: UUID,
    company_id: UUID,
    type_id: UUID,
) -> None:
    result = await firmware_repo.check_firmware_belongs_to(
        firmware_id=firmware_id, company_id=company_id, type_id=type_id
    )

    if not result:
        raise ObjectNotFoundError(object_id=firmware_id)
