from calypte_api.models import TimeStampAbstract, UUIDAbstract
from device_group.models import DeviceGroup
from django.db import models


class FirmwareInfo(UUIDAbstract, TimeStampAbstract):  # type: ignore
    version: models.CharField = models.CharField(max_length=255)
    serial_number: models.CharField = models.CharField(max_length=255, unique=True)
    group: models.ForeignKey = models.ForeignKey(DeviceGroup, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.version
