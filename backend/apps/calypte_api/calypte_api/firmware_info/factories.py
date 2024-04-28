from firmware_info.models import FirmwareInfo

from device_group.models import DeviceGroup
from factory import Faker, Iterator, Sequence
from factory.django import DjangoModelFactory


class FirmwareInfoFactory(DjangoModelFactory):
    class Meta:
        model = FirmwareInfo

    version: Sequence = Sequence(lambda n: f"v0.{n}.0")
    serial_number: Faker = Faker(
        "password",
        length=64,
        special_chars=True,
        digits=True,
        upper_case=True,
        lower_case=True,
    )
    group: Iterator = Iterator(DeviceGroup.objects.all())
