import factory
from django.utils.crypto import get_random_string

from apps.account.tests.factories import UserFactory
from apps.bookfiller.models.models import BookFiller
from apps.exchange.tests.factories import ApiKeyFactory


class BookFillerFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    side = factory.Faker("side")
    user = factory.SubFactory(UserFactory)
    api_key = factory.SubFactory(ApiKeyFactory)
    pair_token = factory.LazyAttribute(lambda obj: get_random_string(length=64))
    order_size = factory.Faker("order_size")
    number_of_orders = factory.Faker("number_of_orders")
    budget = factory.Faker("budget")
    user_ref_price = factory.Faker("user_ref_price")

    class Meta:
        model = BookFiller
