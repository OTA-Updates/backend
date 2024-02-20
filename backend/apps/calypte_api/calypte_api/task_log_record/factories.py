from task_log_record.models import TaskLogRecord

from factory import Faker
from factory.django import DjangoModelFactory


class TaskLogRecordFactory(DjangoModelFactory):
    class Meta:
        model = TaskLogRecord
        django_get_or_create = ("task",)

    message: Faker = Faker("text")
