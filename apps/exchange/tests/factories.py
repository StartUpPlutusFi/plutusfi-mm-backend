import factory

from apps.exchange.models.models import Exchange, ApiKeys


class ExchangeFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")

    class Meta:
        model = Exchange


class ApiKeyFactory(factory.django.DjangoModelFactory):

    user = factory.Faker("user")
    api_key = factory.Faker("api_key")
    api_secret = factory.Faker("api_secret")
    description = factory.Faker("description")
    default = factory.Faker("default")
    exchange_id = factory.Faker("exchange")

    class Meta:
        model = ApiKeys
