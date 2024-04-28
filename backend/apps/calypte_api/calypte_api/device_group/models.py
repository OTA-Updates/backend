from calypte_api.models import TimeStampAbstract, UUIDAbstract
from django.db import models
from protocol.models import Protocol


class DeviceGroup(UUIDAbstract, TimeStampAbstract):  # type: ignore
    name: models.CharField = models.CharField(max_length=255, unique=True)
    protocol: models.ForeignKey = models.ForeignKey(Protocol, on_delete=models.PROTECT)
    shared_secret: models.CharField = models.CharField(max_length=512, unique=True)

    def __str__(self) -> str:
        return self.name
