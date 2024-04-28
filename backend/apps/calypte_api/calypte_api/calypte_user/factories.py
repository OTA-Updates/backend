from calypte_user.models import CalypteUser

from factory import Faker
from factory.django import DjangoModelFactory


class CalypteUserFactory(DjangoModelFactory):
    class Meta:
        model = CalypteUser

    username: Faker = Faker("user_name")
    email: Faker = Faker("email")
    password: Faker = Faker("password")
