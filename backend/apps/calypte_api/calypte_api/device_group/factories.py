from device_group.models import DeviceGroup

from factory import Faker, Iterator
from factory.django import DjangoModelFactory
from protocol.models import Protocol


class DeviceGroupFactory(DjangoModelFactory):
    class Meta:
        model = DeviceGroup

    # id: Faker = Faker("uuid4")
    name: Faker = Faker("word")
    protocol: Iterator = Iterator(Protocol.objects.all())
    shared_secret: Faker = Faker(
        "password",
        length=64,
        special_chars=True,
        digits=True,
        upper_case=True,
        lower_case=True,
    )
