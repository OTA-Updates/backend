from calypte_api.common.models import (
    BaseModel,
    CompanyMixin,
    TimeStampedMixin,
    UUIDMixin,
)

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Type(BaseModel, CompanyMixin, UUIDMixin, TimeStampedMixin):
    __tablename__ = "types"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )
