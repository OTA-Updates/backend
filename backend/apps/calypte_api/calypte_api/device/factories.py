import datetime

from device.models import Device

from factory import Faker, post_generation
from factory.django import DjangoModelFactory


class DeviceFactory(DjangoModelFactory):
    class Meta:
        model = Device

    name: Faker = Faker("word")
    serial_number: Faker = Faker(
        "password",
        length=64,
        special_chars=True,
        digits=True,
        upper_case=True,
        lower_case=True,
    )
    registration_date: Faker = Faker("date_time", tzinfo=datetime.UTC)
    last_seen: Faker = Faker("date_time")

    @post_generation
    def tags(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.tags.add(*extracted)
