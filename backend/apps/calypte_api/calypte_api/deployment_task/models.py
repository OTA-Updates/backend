from calypte_api.models import TimeStampAbstract, UUIDAbstract
from deployment.models import Deployment
from device.models import Device
from django.db import models
from task_status.models import TaskStatus


class DeploymentTask(UUIDAbstract, TimeStampAbstract):  # type: ignore
    deployment: models.ForeignKey = models.ForeignKey(
        Deployment, on_delete=models.CASCADE, related_name="deployment_tasks"
    )
    device: models.ForeignKey = models.ForeignKey(Device, on_delete=models.PROTECT)
    state: models.ForeignKey = models.ForeignKey(TaskStatus, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{self.deployment} - {self.device}"
