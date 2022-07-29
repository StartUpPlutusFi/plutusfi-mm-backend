import factory

from apps.account.models import User


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker("name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    class Meta:
        model = User
