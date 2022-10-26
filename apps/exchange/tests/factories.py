from random import choice

import factory
from django.utils.crypto import get_random_string

from apps.account.tests.factories import UserFactory
from apps.exchange.models.models import Exchange, ApiKeys


class ExchangeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Exchange


class ApiKeyFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    api_key = factory.LazyAttribute(lambda obj: get_random_string(length=64))
    api_secret = factory.LazyAttribute(lambda obj: get_random_string(length=64))
    description = factory.Faker("text")
    default = factory.LazyAttribute(lambda obj: choice([True, False]))
    exchange = factory.SubFactory(ExchangeFactory)

    class Meta:
        model = ApiKeys
