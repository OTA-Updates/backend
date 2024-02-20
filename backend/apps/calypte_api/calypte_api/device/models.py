from calypte_api.models import TimeStampAbstract, UUIDAbstract
from device_group.models import DeviceGroup
from django.db import models
from firmware_info.models import FirmwareInfo
from tag.models import Tag


class Device(UUIDAbstract, TimeStampAbstract):  # type: ignore
    name: models.CharField = models.CharField(max_length=255)
    serial_number: models.CharField = models.CharField(max_length=255)
    registration_date: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    last_seen: models.DateTimeField = models.DateTimeField(default=None, null=True)

    group: models.ForeignKey = models.ForeignKey(DeviceGroup, on_delete=models.PROTECT)
    firmware: models.ForeignKey = models.ForeignKey(
        FirmwareInfo, on_delete=models.PROTECT, null=True
    )
    tags: models.ManyToManyField = models.ManyToManyField(
        Tag, blank=True, related_name="devices"
    )

    def __str__(self) -> str:
        return self.name
