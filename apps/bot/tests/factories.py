import factory

from apps.dashboard.db.models import MarketMakerBot

class MarketMakerBotFactory(factory.django.DjangoModelFactory):

    name = factory.Faker("name")
    description = factory.Faker("description")
    user = factory.Faker("user")
    api_key = factory.Faker("api_key")
    pair_token = factory.Faker("pair_token")
    trade_qty_range_low = factory.Faker("trade_qty_range_low")
    trade_qty_range_high = factory.Faker("trade_qty_range_high")
    trade_candle = factory.Faker("trade_candle")
    trade_amount = factory.Faker("trade_amount")
    status = factory.Faker("status")
    
    class Meta:
        model = MarketMakerBot
