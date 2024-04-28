from calypte_api.models import TimeStampAbstract, UUIDAbstract
from device_group.models import DeviceGroup
from django.db import models
from firmware_info.models import FirmwareInfo


class Deployment(UUIDAbstract, TimeStampAbstract):  # type: ignore
    name: models.CharField = models.CharField(max_length=255)
    group: models.ForeignKey = models.ForeignKey(DeviceGroup, on_delete=models.PROTECT)
    firmware: models.ForeignKey = models.ForeignKey(
        FirmwareInfo, on_delete=models.PROTECT, null=True
    )
    scheduled_date: models.DateTimeField = models.DateTimeField(default=None, null=True)
    completion_date: models.DateTimeField = models.DateTimeField(
        default=None, null=True
    )

    def __str__(self) -> str:
        return self.name
