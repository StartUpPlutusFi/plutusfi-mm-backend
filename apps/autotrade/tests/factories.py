import factory

from random import choice

import factory
from django.utils.crypto import get_random_string

from apps.autotrade.models.models import MarketMakerBot
from apps.account.tests.factories import UserFactory
from apps.exchange.tests.factories import ApiKeyFactory


class MMFactory(factory.django.DjangoModelFactory):
    photo = factory.django.ImageField(width=1024, height=768)
    name = factory.Faker("name")
    description = factory.Faker("description")
    user = factory.SubFactory(UserFactory)
    api_key = factory.SubFactory(ApiKeyFactory)
    pair_token = factory.LazyAttribute(lambda obj: get_random_string(length=8))
    user_ref_price = factory.Faker("user_ref_price")
    side = factory.Faker("side")
    trade_candle = factory.Faker("trade_candle")
    trade_amount = factory.Faker("trade_amount")
    status = factory.LazyAttribute(lambda obj: choice([True, False]))

    class Meta:
        model = MarketMakerBot
