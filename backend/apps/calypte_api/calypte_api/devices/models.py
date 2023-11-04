from datetime import datetime
from typing import TYPE_CHECKING

from calypte_api.common.models import (
    BaseModel,
    CompanyMixin,
    TimeStampedMixin,
    UUIDMixin,
)
from calypte_api.firmware_info.models import FirmwareInfo
from calypte_api.groups.models import Group
from calypte_api.types.models import Type

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


if TYPE_CHECKING:
    pass


class Device(CompanyMixin, UUIDMixin, TimeStampedMixin, BaseModel):
    __tablename__ = "devices"

    type_id: Mapped[Type] = mapped_column(
        ForeignKey("types.id", ondelete="CASCADE")
    )
    current_firmware_id: Mapped[FirmwareInfo | None] = mapped_column(
        ForeignKey("firmware_info.id", ondelete=None), nullable=True
    )
    group_id: Mapped[Group] = mapped_column(
        ForeignKey("groups.id", ondelete=None)
    )

    serial_number: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    registered_at: Mapped[datetime | None] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"<Device {self.name}>"
