import factory

from apps.bookfiller.models.models import BookFiller


class BookFillerFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    side = factory.Faker("side")
    user = factory.Faker("user")
    api_key = factory.Faker("api_key")
    pair_token = factory.Faker("pair_token")
    order_size = factory.Faker("order_size")
    number_of_orders = factory.Faker("number_of_orders")
    budget = factory.Faker("budget")
    user_ref_price = factory.Faker("user_ref_price")

    class Meta:
        model = BookFiller
