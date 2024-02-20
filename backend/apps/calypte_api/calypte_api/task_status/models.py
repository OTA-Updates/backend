from calypte_api.models import TimeStampAbstract, UUIDAbstract
from django.db import models


class TaskStatusChoices(models.IntegerChoices):
    PLANNED = 2
    PENDING = 3
    RUNNING = 4
    COMPLETED = 5
    FAILED = 1


class TaskStatus(UUIDAbstract, TimeStampAbstract):  # type: ignore
    state: models.IntegerField = models.IntegerField(
        null=False,
        blank=False,
        choices=TaskStatusChoices,
    )

    def __str__(self) -> str:
        return TaskStatusChoices(self.state).label
