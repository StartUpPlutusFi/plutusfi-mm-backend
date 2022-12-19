import factory
from django.utils.crypto import get_random_string

from apps.account.tests.factories import UserFactory
from apps.exchange.tests.factories import ApiKeyFactory
from apps.orderLimit.models.models import OrderLimit


class OrderLimitFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    user = factory.SubFactory(UserFactory)
    api_key_id = factory.SubFactory(ApiKeyFactory)
    side = factory.Faker("side")
    pair_token = factory.LazyAttribute(lambda obj: get_random_string(length=64))
    quantity = factory.Faker("order_size")
    price = factory.Faker("order_size")
    status = factory.Faker("order_size")

    class Meta:
        model = OrderLimit
