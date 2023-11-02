#
# TODO: adds color field to the tag model
from typing import TYPE_CHECKING

from calypte_api.common.models import (
    BaseModel,
    CompanyMixin,
    TimeStampedMixin,
    UUIDMixin,
    device_tag_lookup,
)
from calypte_api.types.models import Type

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from calypte_api.devices.models import Device


class Tag(CompanyMixin, UUIDMixin, TimeStampedMixin, BaseModel):
    __tablename__ = "tags"

    type_id: Mapped[Type] = mapped_column(
        ForeignKey("types.id", ondelete="CASCADE")
    )

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    color: Mapped[str] = mapped_column(String(10), nullable=True)

    devices: Mapped[list["Device"]] = relationship(
        secondary=device_tag_lookup, back_populates="tags"
    )

    def __repr__(self) -> str:
        return f"<Device {self.name}>"
