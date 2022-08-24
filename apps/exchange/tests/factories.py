import factory

from apps.exchange.db import Exchange


class ExchangeFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")

    class Meta:
        model = Exchange
