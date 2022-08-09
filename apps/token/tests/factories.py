import factory

from apps.dashboard.db.models import BotConfigPairtokens


class TokenFactory(factory.django.DjangoModelFactory):
    pair = factory.Faker("pair")

    class Meta:
        model = BotConfigPairtokens
