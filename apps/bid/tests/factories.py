import factory

from apps.dashboard.db.models import BidBot


class BidBotFactory(factory.django.DjangoModelFactory):

    name = factory.Faker("name")
    description = factory.Faker("description")
    user = factory.Faker("user")
    api_key = factory.Faker("api_key")
    pair_token = factory.Faker("pair_token")
    order_size = factory.Faker("order_size")
    number_of_orders = factory.Faker("number_of_orders")
    budget = factory.Faker("budget")
    trade_amount = factory.Faker("trade_amount")
    status = factory.Faker("status")

    class Meta:
        model = BidBot
