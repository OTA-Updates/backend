from calypte_api.common.models import (
    BaseModel,
    CompanyMixin,
    TimeStampedMixin,
    UUIDMixin,
)
from calypte_api.types.models import Type

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


class FirmwareInfo(BaseModel, CompanyMixin, TimeStampedMixin, UUIDMixin):
    __tablename__ = "firmware_info"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    version: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    type_id: Mapped[Type] = mapped_column(
        ForeignKey("types.id", ondelete="CASCADE")
    )

    def __repr__(self) -> str:
        return f"<FirmwareInfo {self.name}>"
