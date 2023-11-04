import uuid

from datetime import datetime
from typing import TYPE_CHECKING

from calypte_api.common.settings import get_settings

from sqlalchemy import MetaData
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


if TYPE_CHECKING:
    pass


settings = get_settings()


class BaseModel(AsyncAttrs, DeclarativeBase):
    metadata = MetaData(schema=settings.postgres_schema)


class CompanyMixin:
    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )


class UUIDMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        primary_key=True,
        default=uuid.uuid4,
    )


class TimeStampedMixin:
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )
