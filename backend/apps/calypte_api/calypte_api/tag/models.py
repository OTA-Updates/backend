from calypte_api.models import TimeStampAbstract, UUIDAbstract
from colorfield.fields import ColorField  # type: ignore
from django.db import models


class Tag(UUIDAbstract, TimeStampAbstract):  # type: ignore
    name: models.CharField = models.CharField(max_length=255, null=False, blank=False)
    color: ColorField = ColorField(default="#FF0000")
