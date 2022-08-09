# from django.test import TestCase

# # Create your tests here.
from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from apps.account.tests.factories import UserFactory
from apps.exchange_api.tests.factories import ApiKeyFactory, ExchangeFactory
from apps.token.tests.factories import TokenFactory
from apps.bot.tests.factories import MarketMakerBotFactory

from apps.dashboard.db.models import MarketMakerBot


# Create your tests here.
class TestMMbotBot(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.user = UserFactory.create(password="abc123@", username="testSS")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.exchange = ExchangeFactory(name="ScamEx")

        self.token = TokenFactory(pair="FakeToken")

        self.api = ApiKeyFactory.create(
            description="2222222222222",
            user=self.user,
            api_key="222222222222",
            api_secret="222222222222",
            default=False,
            exchange=self.exchange,
        )

        self.MMbot = MarketMakerBotFactory(
            name="MM bot 1",
            description="MM bot 1",
            user=self.user,
            api_key=self.api,
            pair_token=self.token,
            trade_qty_range_low=33,
            trade_qty_range_high=40,
            trade_candle=15,
            trade_amount=11,
            status="STOP",
        )

    def test_add_MMbot(self):
        data = {
            "name": "MM_bot",
            "description": "MM",
            "trade_qty_range_low": 33,
            "trade_qty_range_high": 40,
            "trade_candle": 15,
            "trade_amount": 11.0,
            "status": "STOP",
            "api_key": self.api.id,
            "pair_token": self.token.id,
        }

        # print(data)

        request = self.client.post(reverse("MMbot:MMbotAdd"), data)

        # print(request.data)

        self.assertEqual(request.status_code, 200)
        # self.assertEqual(request.json(), data)
        # self.assertEqual(request.json()['user'], data['user'])
        self.assertEqual(request.json()["api_key"], data["api_key"])

    def test_add_MMbot_wth_wrong_parameter(self):
        data = {
            "wrong_name_lmao": "fake_ex",
            "pair_token": self.token,
            "trade_qty_range_low": 33,
            "trade_qty_range_high": 40,
            "trade_candle": 15,
            "trade_amount": 11,
            "api_key": "",
            "user": 1,
        }

        request = self.client.post(reverse("MMbot:MMbotAdd"), data)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()["code"], 5)

    def test_get_all_MMbot(self):

        data = list(MarketMakerBot.objects.all().values())
        request = self.client.get(reverse("MMbot:MMbotList"))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json()), len(data))

    def test_detail_MMbot(self):

        data = MarketMakerBot.objects.first()
        request = self.client.get(reverse("MMbot:MMbotDetail", kwargs={"pk": data.id}))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()[0]["name"], data.name)

    def test_detail_MMbot_with_invalid_id(self):

        request = self.client.get(
            reverse("MMbot:MMbotDetail", kwargs={"pk": 922337203685477580})
        )
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json(), [])

    def test_update_MMbot(self):

        data = MarketMakerBot.objects.first()
        update = {
            "name": "MM bot 1",
            "description": "MM bot 1",
            "api_key": self.api.id,
            "pair_token": self.token.id,
            "trade_qty_range_low": 33,
            "trade_qty_range_high": 40,
            "trade_candle": 15,
            "trade_amount": 11,
            "status": "START",
        }

        request = self.client.put(
            reverse("MMbot:MMbotUpdate", kwargs={"pk": data.id}), data=update
        )
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()["status"], update["status"])

    def test_update_MMbot_with_invalid_paramter(self):

        update = {
            "clover_fake": "Nwe scam test",
        }

        request = self.client.put(
            reverse("MMbot:MMbotUpdate", kwargs={"pk": 922337203685477580}), data=update
        )
        self.assertEqual(request.status_code, 200)
        self.assertIsNot(request.json(), [])

    def test_delete_MMbot(self):

        data = MarketMakerBot.objects.first()
        request = self.client.delete(
            reverse("MMbot:MMbotDelete", kwargs={"pk": data.id})
        )
        self.assertEqual(request.status_code, 204)

    def test_delete_MMbot_with_invalid_id(self):

        request = self.client.delete(
            reverse("MMbot:MMbotDelete", kwargs={"pk": 922337203685477580})
        )
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()["code"], 5)
