from calypte_api.models import TimeStampAbstract, UUIDAbstract
from deployment_task.models import DeploymentTask
from django.db import models


class TaskLogRecord(UUIDAbstract, TimeStampAbstract):  # type: ignore
    message: models.TextField = models.TextField(null=False, blank=False)
    task: models.ForeignKey = models.ForeignKey(
        DeploymentTask, on_delete=models.PROTECT
    )
