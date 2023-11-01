import uuid

from datetime import datetime
from typing import TYPE_CHECKING

from calypte_api.common.settings import get_settings

from sqlalchemy import Column, ForeignKey, MetaData, Table, UniqueConstraint
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


device_tag_lookup = Table(
    "device_tag_lookup",
    BaseModel.metadata,
    Column("id", UUID(), primary_key=True, default=uuid.uuid4),
    Column("device_id", UUID(), ForeignKey("devices.id", ondelete="CASCADE")),
    Column("tag_id", UUID(), ForeignKey("tags.id", ondelete="CASCADE")),
    UniqueConstraint(
        "device_id", "tag_id", name="uq_device_tag_lookup_device_id_tag_id"
    ),
)


# class DeviceFirmwareLookup(BaseModel, TimeStampedMixin, UUIDMixin):
#     __tablename__ = "device_firmware_lookup"
#     __table_args__ = (
#         UniqueConstraint(
#             "device_id",
#             "firmware_info_id",
#             name="uq_device_firmware_lookup_device_id_firmware_info_id",
#         ),
#     )

#     device_id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True),
#         ForeignKey("devices.id"),
#         nullable=False,
#     )
#     firmware_info_id: Mapped[uuid.UUID | None] = mapped_column(
#         UUID(as_uuid=True),
#         ForeignKey("firmware_info.id"),
#         nullable=False,
#     )

#     device: Mapped["Device"] = relationship(
#         "Device", back_populates="firmware_info"
#     )
#     firmware_info: Mapped["FirmwareInfo"] = relationship(
#         "FirmwareInfo", back_populates="devices"
#     )
