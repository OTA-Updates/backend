from calypte_api.models import TimeStampAbstract, UUIDAbstract
from django.db import models


class Protocol(UUIDAbstract, TimeStampAbstract):  # type: ignore
    name: models.CharField = models.CharField(max_length=255, unique=True)
