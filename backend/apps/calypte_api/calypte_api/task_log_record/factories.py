from task_log_record.models import TaskLogRecord

from deployment_task.models import DeploymentTask
from factory import Faker, Iterator
from factory.django import DjangoModelFactory


class TaskLogRecordFactory(DjangoModelFactory):
    class Meta:
        model = TaskLogRecord

    message: Faker = Faker("text")
    task: Iterator = Iterator(DeploymentTask.objects.all())
