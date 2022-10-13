# from django.test import TestCase

# # Create your tests here.
from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from apps.account.tests.factories import UserFactory
from apps.autotrade.tests.factories import MMFactory
from apps.exchange.tests.factories import ExchangeFactory, ApiKeyFactory

from apps.autotrade.models.models import *


class TestAutoTrade(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory.create(password="abc123@", username="testSS")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.exchange = ExchangeFactory(name="ScamEx")

        self.api = ApiKeyFactory(
            description="test",
            user=self.user,
            api_key="0x0000000000",
            api_secret="0x11111111",
            default=False,
            exchange=self.exchange,
        )

        self.mmbot = MMFactory(
            name="Name",
            description="description test",
            pair_token="DUMMY",
            user_ref_price=100,
            side=1,
            trade_candle=10,
            trade_amount=0.1,
            api_key_id=self.api.id,
            user_id=self.user.id,
            status="STOP",
        )

    # def test_add_autotrade(self):
    #     data = {
    #         "name": "big auto",
    #         "description": "test",
    #         "pair_token": "AuV-USDT",
    #         "user_ref_price": 0.0,
    #         "side": 2,
    #         "trade_candle": 1,
    #         "trade_amount": 12.0,
    #         "api_key_id": self.api.id
    #     }
    #
    #     request = self.client.post(reverse("MMbot:MMbotAdd"), data)
    #     print(request.json(), data)
    #
    #     self.assertEqual(request.status_code, 200)
    #     self.assertDictEqual(request.json(), {})

    def test_get_all_bots_by_user(self):
        data = MarketMakerBot.objects.filter(user_id=self.user.id).values()
        request = self.client.get(reverse("MMbot:MMbotList"))
        # print('test_get_all_bots_by_user', request.json())
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json()), len(data))

    def test_detail_bots_by_id(self):
        data = MarketMakerBot.objects.filter(user_id=self.user.id, id=self.mmbot.id).values().first()
        request = self.client.get(
            reverse("MMbot:MMbotDetail", kwargs={"pk": data['id']})
        )

        # print('test_detail_bots_by_id', request.json(), data)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()[0]['id'], data['id'])
        self.assertEqual(request.json()[0]['pair_token'], data['pair_token'])
        self.assertEqual(request.json()[0]['trade_candle'], data['trade_candle'])
        self.assertEqual(request.json()[0]['status'], data['status'])

    def test_detail_bots_by_id_wth_invalid_id(self):
        request = self.client.get(
            reverse("MMbot:MMbotDetail", kwargs={"pk": 999999})
        )

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json(), [])

    #
    def test_update_autotrade_with_right_parameter(self):
        update = {
            "name": "wwwww",
            "description": "cass_bot",
            "trade_qty_range_low": 10,
            "trade_qty_range_high": 12,
            "trade_candle": 1,
            "trade_amount": 999.0,
            "status": "0",
            "api_key_id": 1
        }

        request = self.client.put(
            reverse("MMbot:MMbotUpdate", kwargs={"pk": 922337203685477580}),
            data=update,
        )

        expected_response = {
            "name": "",
            "description": "",
            "pair_token": "",
            "user_ref_price": None,
            "side": None,
            "trade_candle": None,
            "trade_amount": None,
            "status": "",
            "user": None,
            "api_key": None
        }

        self.assertEqual(request.status_code, 400)
        self.assertDictEqual(request.json(), expected_response)

    def test_update_autotrade_with_invalid_parameter(self):
        update = {
            "name": "wwwww",
            "description": "cass_bot",
            "trade_qty_range_low": 10,
            "trade_qty_range_high": 12,
            "trade_candle": 1,
            "trade_amount": 999.0,
            "status": "0",
            "api_key_id": 1
        }

        request = self.client.put(
            reverse("MMbot:MMbotUpdate", kwargs={"pk": 922337203685477580}),
            data=update,
        )

        expected_response_error = {
            'code': "Field 'id' expected a number but got ['1'].",
            'msg': 'invalid data or unauthorized api_key_id',
            'status': 'error'
        }

        self.assertEqual(request.status_code, 400)
        self.assertDictEqual(request.json(), expected_response_error)

    def test_delete_apikey(self):
        data = MarketMakerBot.objects.filter(user_id=self.user.id, id=self.mmbot.id).first()
        request = self.client.delete(
            reverse("MMbot:MMbotDelete", kwargs={"pk": data.id})
        )

        expected_response = {'status': 'done'}

        self.assertEqual(request.status_code, 200)
        self.assertDictEqual(request.json(), expected_response)

    def test_delete_apikey_with_invalid_id(self):
        request = self.client.delete(
            reverse("MMbot:MMbotDelete", kwargs={"pk": 922337203685477580})
        )

        expected_response = {'status': 'data not found'}

        self.assertEqual(request.status_code, 404)
        self.assertDictEqual(request.json(), expected_response)
