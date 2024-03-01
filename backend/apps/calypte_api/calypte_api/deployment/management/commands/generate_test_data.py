import random

from deployment.factories import DeploymentFactory
from deployment.models import Deployment

from deployment_task.factories import DeploymentTaskFactory
from deployment_task.models import DeploymentTask
from device.factories import DeviceFactory
from device.models import Device
from device_group.factories import DeviceGroupFactory
from device_group.models import DeviceGroup
from django.core.management.base import BaseCommand
from faker import Faker as RawFaker
from firmware_info.factories import FirmwareInfoFactory
from firmware_info.models import FirmwareInfo
from protocol.models import Protocol, ProtocolChoices
from tag.factories import TagFactory
from tag.models import Tag
from task_log_record.factories import TaskLogRecordFactory
from task_log_record.models import TaskLogRecord
from task_status.models import TaskStatus, TaskStatusChoices


class Command(BaseCommand):
    help = "Generate test data for the Calypte API."

    def add_arguments(self, parser):
        ...

    def generate_task_statuses(self) -> list[TaskStatus]:
        for status in TaskStatusChoices:
            TaskStatus.objects.get_or_create(state=status)

        return list(TaskStatus.objects.all())

    def generate_protocols(self) -> list[Protocol]:
        for protocol in ProtocolChoices:
            Protocol.objects.get_or_create(name=protocol.value)

        return list(Protocol.objects.all())

    def generate_device_groups(self, size: int) -> list[DeviceGroup]:
        DeviceGroupFactory.create_batch(size=size)

        return list(DeviceGroup.objects.all())

    def generate_firmware_info(self, size: int) -> list[FirmwareInfo]:
        FirmwareInfoFactory.create_batch(size=size)

        return list(FirmwareInfo.objects.all())

    # TODO: fix each device add all tags
    def generate_devices(self, groups: list[DeviceGroup], size: int) -> list[Device]:
        for group in groups:
            tags = random.choices(
                Tag.objects.filter(group=group), k=random.randint(0, 5)
            )

            firmware = FirmwareInfo.objects.filter(group=group).first()
            DeviceFactory.create_batch(
                size=size, group=group, tags=tags, firmware=firmware
            )

        return list(Device.objects.all())

    def generate_tags(self, size: int) -> list[Tag]:
        TagFactory.create_batch(size=size)

        return list(Tag.objects.all())

    def generate_deployments(
        self, groups: list[DeviceGroup], size: int
    ) -> list[Deployment]:
        faker = RawFaker()
        for group in groups:
            firmware = FirmwareInfo.objects.filter(group=group).first()
            scheduled_date = faker.date_between(start_date="-3y", end_date="today")
            completion_date = (
                None
                if faker.boolean()
                else faker.date_time_between(start_date=scheduled_date, end_date="now")
            )
            DeploymentFactory.create_batch(
                size=size,
                group=group,
                firmware=firmware,
                scheduled_date=scheduled_date,
                completion_date=completion_date,
            )

        return list(Deployment.objects.all())

    def generate_deployment_tasks(
        self, groups: list[DeviceGroup], size: int
    ) -> list[DeploymentTask]:
        for group in groups:
            device = random.choice(Device.objects.filter(group=group))
            deployment = random.choice(Deployment.objects.filter(group=group))
            DeploymentTaskFactory.create_batch(
                size=size, deployment=deployment, device=device
            )

        return list(DeploymentTask.objects.all())

    def generate_task_log_records(self, size: int) -> list[TaskLogRecord]:
        TaskLogRecordFactory.create_batch(size=size)

        return list(TaskLogRecord.objects.all())

    def delete_all_data(self) -> None:
        TaskLogRecord.objects.all().delete()
        DeploymentTask.objects.all().delete()
        TaskStatus.objects.all().delete()
        Deployment.objects.all().delete()
        Device.objects.all().delete()
        FirmwareInfo.objects.all().delete()
        DeviceGroup.objects.all().delete()
        Protocol.objects.all().delete()
        Tag.objects.all().delete()

    def handle(self, *args, **options):
        self.delete_all_data()

        self.generate_task_statuses()
        self.generate_protocols()
        device_groups = self.generate_device_groups(size=10)
        self.generate_firmware_info(size=30)
        self.generate_tags(size=15)
        self.generate_devices(groups=device_groups, size=50)
        self.generate_deployments(groups=device_groups, size=10)
        self.generate_deployment_tasks(groups=device_groups, size=10)
        self.generate_task_log_records(size=1000)

        self.stdout.write(self.style.SUCCESS("Successfully generated test data."))
