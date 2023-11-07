from uuid import UUID

from calypte_api.common.commands import ICommand
from calypte_api.firmware.schemas import (
    CreateFirmwareRequestBody,
    CreateFirmwareResponse,
)
from calypte_api.firmware.uow import IUOWFirmware


class CreateFirmwareCommand(ICommand):
    def __init__(
        self,
        uow: IUOWFirmware,
        company_id: UUID,
        request_type: CreateFirmwareRequestBody,
    ) -> None:
        self.uow = uow
        self.company_id = company_id
        self.request_type = request_type

    async def execute(self) -> CreateFirmwareResponse:
        # * Calls' order is play crucial role here
        async with self.uow:
            firmware_info = await self.uow.sql_repo.create_firmware(
                company_id=self.company_id,
                type_id=self.request_type.type_id,
                serial_number=self.request_type.serial_number,
                name=self.request_type.name,
                description=self.request_type.description,
                version=self.request_type.version,
            )
            await self.uow.s3_repo.upload_firmware(
                company_id=self.company_id,
                firmware_id=firmware_info.id,
                firmware=self.request_type.firmware,
            )
            self.uow.commit()

            return firmware_info

    async def rollback(self):
        ...
