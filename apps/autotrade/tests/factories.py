import factory

from apps.autotrade.models.models import MarketMakerBot


class MMFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    description = factory.Faker("description")
    user_id = factory.Faker("user_id")
    api_key_id = factory.Faker("api_key_id")
    pair_token = factory.Faker("pair_token")
    user_ref_price = factory.Faker("user_ref_price")
    side = factory.Faker("side")
    trade_candle = factory.Faker("trade_candle")
    trade_amount = factory.Faker("trade_amount")
    status = factory.Faker("status")

    class Meta:
        model = MarketMakerBot
