from tag.models import Tag

from factory import Faker, post_generation
from factory.django import DjangoModelFactory


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    id: Faker = Faker("uuid4")
    name: Faker = Faker("word")
    color: Faker = Faker("color")

    @post_generation
    def devices(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.devices.add(*extracted)
