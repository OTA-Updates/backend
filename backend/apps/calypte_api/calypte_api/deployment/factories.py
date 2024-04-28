from deployment.models import Deployment

from factory import Faker
from factory.django import DjangoModelFactory


class DeploymentFactory(DjangoModelFactory):
    class Meta:
        model = Deployment

    name: Faker = Faker("word")
