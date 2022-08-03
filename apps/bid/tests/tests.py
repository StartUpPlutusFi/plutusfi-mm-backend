# from django.test import TestCase

# # Create your tests here.
from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from apps.account.tests.factories import UserFactory
from apps.exchange_api.tests.factories import ApiKeyFactory, ExchangeFactory
from apps.token.tests.factories import TokenFactory
from apps.bid.tests.factories import BidBotFactory
from apps.dashboard.db.models import BidBot


# Create your tests here.
class TestBidBot(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory.create(password="abc123@", username="testSS")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.exchange = ExchangeFactory(
            name = "ScamEx"
        )

        self.token = TokenFactory (
            pair = "FakeToken"
        ) 

        self.api = ApiKeyFactory.create(
            description = "2222222222222",
            user = self.user,
            api_key = "222222222222",
            api_secret = "222222222222",
            default = False,
            exchange = self.exchange
        )


        self.bidbot = BidBotFactory(
            name = "fake_bid_bot",
            description = "fake_desc",
            user = self.user,
            api_key = self.api,
            pair_token = self.token,
            order_size = 3300,
            number_of_orders = 2,
            budget = 600,
            trade_amount = 500,
            status = 0,
        )

    def test_add_bidbot(self):
        data = {
            "name": "fake_bid_bot",
            "description": "fake_desc",
            "user": self.user.id,
            "api_key": self.api.id,
            "pair_token": self.token.id,
            "order_size": 3300,
            "number_of_orders": 2,
            "budget": 600,
            "trade_amount": 500,
            "status": 0,
        }

        request = self.client.post(reverse("bidbot:BidAdd"), data)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()['name'], data['name'])
        self.assertEqual(request.json()['user'], data['user'])
        self.assertEqual(request.json()['api_key'], data['api_key'])
    
    def test_add_bidbot_wth_wrong_parameter(self):
        data = {
            "wrong_name_lmao": "fake_ex",
            "user": self.user,
            "api_key": self.api.id,
            "pair_token": self.token.id,
            "order_size": 3300,
            "number_of_orders": 2,
            "budget": 600.0,
            "trade_amount": 500.0,
            "status": 0,
           
        }

        request = self.client.post(reverse("bidbot:BidAdd"), data)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()["code"], 2)

    def test_get_all_BidBot(self):

        data =  list(BidBot.objects.all().values())
        request = self.client.get(reverse("bidbot:BidList"))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json()), len(data))

    def test_detail_bidbot(self):

        data =  BidBot.objects.first()
        request = self.client.get(reverse("bidbot:BidDetail", kwargs={"pk": data.id }))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()[0]['name'], data.name )

    def test_detail_bidbot_with_invalid_id(self):

        request = self.client.get(reverse("bidbot:BidDetail", kwargs={"pk": 999999999999999999999 }))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json(), [] )

    def test_update_bidbot(self):

        data =  BidBot.objects.first()
        
        update = {
            "name": "Nwe scam test",
            "description": "fake_desc",
            "user": self.user.id,
            "api_key": self.api.id,
            "pair_token": self.token.id,
            "order_size": 3200,
            "number_of_orders": 29,
            "budget": 200,
            "trade_amount": 100,
            "status": 0,
        }

        request = self.client.put(reverse("bidbot:BidUpdate", kwargs={"pk": data.id }), data=update)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()['name'], update['name'] )
        self.assertEqual(request.json()['api_key'], update['api_key'] )
        self.assertEqual(request.json()['order_size'], update['order_size'] )
        self.assertEqual(request.json()['trade_amount'], update['trade_amount'] )

    def test_update_bidbot_with_invalid_paramter(self):

        update = {
            "clover_fake": "Nwe scam test",
        }

        request = self.client.put(reverse("bidbot:BidUpdate", kwargs={"pk": 99999999999999999999999999 }), data=update)
        self.assertEqual(request.status_code, 200)
        self.assertIsNot(request.json(), [])

    def test_delete_bidbot(self):

        data =  BidBot.objects.first()
        request = self.client.delete(reverse("bidbot:BidDelete", kwargs={"pk": data.id }))
        self.assertEqual(request.status_code, 204)
    
    def test_delete_bidbot_with_invalid_id(self):

        request = self.client.delete(reverse("bidbot:BidDelete", kwargs={"pk": 99999999999999999999999999 }))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()['code'], 5 )