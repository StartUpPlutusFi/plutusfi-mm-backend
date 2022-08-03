import factory

from apps.dashboard.db.models import ApiKeys, Exchange


class ApiKeyFactory(factory.django.DjangoModelFactory):
    user = factory.Faker("user")
    api_key = factory.Faker("api_key")
    api_secret = factory.Faker("api_secret")
    description = factory.Faker("description")
    default = factory.Faker("default")
    exchange = factory.Faker("exchange")
    
    class Meta:
        model = ApiKeys

class ExchangeFactory(factory.django.DjangoModelFactory):

    name = factory.Faker("name")

    class Meta:
        model = Exchange
