from datetime import datetime
from typing import TYPE_CHECKING

from calypte_api.common.models import (
    BaseModel,
    CompanyMixin,
    TimeStampedMixin,
    UUIDMixin,
    device_tag_lookup,
)
from calypte_api.firmware_info.models import FirmwareInfo
from calypte_api.types.models import Type

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from calypte_api.tags.models import Tag


class Device(CompanyMixin, UUIDMixin, TimeStampedMixin, BaseModel):
    __tablename__ = "devices"

    type_id: Mapped[Type] = mapped_column(
        ForeignKey("types.id", ondelete="CASCADE")
    )
    firmware_info_id: Mapped[FirmwareInfo] = mapped_column(
        ForeignKey("firmware_info.id", ondelete=None)
    )

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    registered_at: Mapped[datetime | None] = mapped_column(nullable=True)

    tags: Mapped[list["Tag"]] = relationship(
        secondary=device_tag_lookup, back_populates="devices", lazy="joined"
    )

    def __repr__(self) -> str:
        return f"<Device {self.name}>"
