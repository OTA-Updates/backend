from deployment_task.models import DeploymentTask

from factory import Iterator
from factory.django import DjangoModelFactory
from task_status.models import TaskStatus


class DeploymentTaskFactory(DjangoModelFactory):
    class Meta:
        model = DeploymentTask

    state: Iterator = Iterator(TaskStatus.objects.all())
