#
# TODO: adds color field to the tag model
from typing import TYPE_CHECKING

from calypte_api.common.models import (
    BaseModel,
    CompanyMixin,
    TimeStampedMixin,
    UUIDMixin,
)
from calypte_api.types.models import Type

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


if TYPE_CHECKING:
    ...


class Group(CompanyMixin, UUIDMixin, TimeStampedMixin, BaseModel):
    __tablename__ = "groups"

    type_id: Mapped[Type] = mapped_column(
        ForeignKey("types.id", ondelete="CASCADE"), nullable=False
    )

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Group {self.name}>"
