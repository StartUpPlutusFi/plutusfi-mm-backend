import factory

from apps.dashboard.db.models import Exchange

class ExchangeFactory(factory.django.DjangoModelFactory):

    name = factory.Faker("name")

    class Meta:
        model = Exchange
