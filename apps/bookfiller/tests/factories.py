import factory

from apps.bookfiller.models.models import BookFiller


class BookFillerFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    side = factory.Faker("side")
    user_id = factory.Faker("user")
    api_key_id = factory.Faker("api_key")
    pair_token = factory.Faker("pair_token")
    order_size = factory.Faker("order_size")
    number_of_orders = factory.Faker("number_of_orders")
    budget = factory.Faker("budget")
    user_ref_price = factory.Faker("user_ref_price")
    status = factory.Faker("status")

    class Meta:
        model = BookFiller
