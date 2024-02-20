from calypte_api.models import TimeStampAbstract, UUIDAbstract
from django.db import models


class TaskStatusChoices(models.TextChoices):
    PLANNED = "PLANNED", "PLANNED"
    PENDING = "PENDING", "PENDING"
    RUNNING = "RUNNING", "RUNNING"
    COMPLETED = "COMPLETED", "COMPLETED"
    FAILED = "FAILED", "FAILED"


class TaskStatus(UUIDAbstract, TimeStampAbstract):  # type: ignore
    state: models.CharField = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        choices=TaskStatusChoices,
    )
