from tag.models import Tag

from device_group.models import DeviceGroup
from factory import Faker, Iterator, post_generation
from factory.django import DjangoModelFactory


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name: Faker = Faker("word")
    color: Faker = Faker("color")
    group: Iterator = Iterator(DeviceGroup.objects.all())

    @post_generation
    def devices(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.devices.add(*extracted)
