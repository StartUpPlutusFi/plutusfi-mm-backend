from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from apps.autotrade.tests.factories import *
from apps.exchange.tests.factories import *


import io
import PIL.Image as Image

class TestAutoTrade(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory.create(password="abc123@", username="testSS")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.exchange = ExchangeFactory.create()

        self.API = ApiKeyFactory.create(
            user=self.user,
            exchange_id=self.exchange.id,
        )

        self.autotrade = MMFactory.create(
            photo=self.gen_image(),
            name="Test Autotrade",
            description="Generic",
            user=self.user,
            api_key=self.API,
            pair_token="TESTDUMMY",
            user_ref_price=100,
            side=1,
            trade_candle=10,
            trade_amount=100.99,
            status="STOP",
        )
    
    @staticmethod
    def gen_image(color=(255, 255, 255)):
        file = io.BytesIO()
        image = Image.new("RGBA", size=(100, 100), color=color)
        image.save(file, "png")
        file.name = "test.png"
        file.seek(0)
        return file

    def test_add_autotrade(self):
        data = {
            "photo": self.gen_image(),
            "name": "Test Autotrade",
            "description": "Generic",
            "user": self.user,
            "api_key": self.API,
            "pair_token": "TESTDUMMY",
            "user_ref_price": 100,
            "side": 1,
            "trade_candle": 10,
            "trade_amount": 100.99,
            "status": "STOP",
        }

        request = self.client.post(reverse("autotrade:MMbotAdd"), data)

        self.assertEqual(request.status_code, 201)
        request_data = request.json()
        self.assertIsNotNone(request.json()["photo"])

        self.assertEqual(request_data["name"], data["name"])
        self.assertEqual(request_data["user"], data["user"])

    # def test_add_autotrade_wth_wrong_parameter(self):
    #     data = {
    #         "photo": self.gen_image(),
    #         "name": "Test Autotrade",
    #         "description": "Generic",
    #         "user": self.user,
    #         "api_key": self.API.api_key,
    #         "pair_token": "TESTDUMMY",
    #         "user_ref_price": b"100",
    #         "side": "char",
    #         "trade_candle": 10,
    #         "trade_amount": 100.99,
    #         "status": "STOP",
    #     }

    #     request = self.client.post(reverse("autotrade:MMbotAdd"), data)

    #     self.assertEqual(request.status_code, 400)
    #     data = request.json()
    #     self.assertEqual(*data.get("name"), "This field is required.")

    # def test_get_all_autotrade(self):
    #     data = MMbot.objects.filter(user_id=self.user.id).values()
    #     request = self.client.get(reverse("autotrade:MMbotList"))
    #     self.assertEqual(request.status_code, 200)
    #     self.assertEqual(len(request.json()), len(data))

    # def test_detail_autotrade(self):
    #     data = MMbot.objects.filter(
    #         user_id=self.user.id, id=self.autotrade.id
    #     ).first()
    #     request = self.client.get(
    #         reverse("autotrade:MMbotDetail", kwargs={"pk": data.id})
    #     )

    #     self.assertEqual(request.status_code, 200)
    #     self.assertEqual(request.json()[0]["name"], data.name)
    #     self.assertEqual(request.json()[0]["side"], data.side)

    # def test_detail_autotrade_with_invalid_id(self):
    #     request = self.client.get(
    #         reverse("autotrade:MMbotDetail", kwargs={"pk": 922337203685477580})
    #     )

    #     self.assertEqual(request.status_code, 200)
    #     self.assertEqual(request.json(), [])

    # def test_update_autotrade_with_invalid_parameter(self):
    #     update = {
    #         "invl": "TEST_USDT_FK",
    #         "api_key": "fake_key000000000000000",
    #         "api_secret": "fake0000000000000000",
    #         "description": "i have pain",
    #         "default": False,
    #         "exchange": self.exchange.id,
    #     }

    #     response = self.client.put(
    #         reverse("autotrade:MMbotUpdate", kwargs={"pk": 922337203685477580}),
    #         data=update,
    #     )

    #     self.assertEqual(response.status_code, 500)
    #     data = response.json()

    #     expected_response = {
    #         "error": True,
    #         "errors": {
    #             "name": "This field is required.",
    #             "side": "This field is required.",
    #             "user_id": "This field is required.",
    #             "order_size": "This field is required.",
    #             "api_key_id": "This field is required.",
    #             "pair_token": "This field is required.",
    #             "number_of_orders": "This field is required.",
    #             "budget": "This field is required.",
    #             "user_ref_price": "This field is required.",
    #         },
    #     }

    #     self.assertDictEqual(data, expected_response)

    # def test_update_autotrade(self):
    #     update = {
    #         "name": "TestMMbot Updated",
    #         "side": 2,
    #         "user_id": self.user.id,
    #         "api_key_id": self.API.id,
    #         "pair_token": "SCAM",
    #         "order_size": 300,
    #         "number_of_orders": 20,
    #         "budget": 1,
    #         "user_ref_price": 0,
    #         "status": "STOP",
    #     }

    #     request = self.client.put(
    #         reverse("autotrade:MMbotUpdate", kwargs={"pk": self.autotrade.id}),
    #         data=update,
    #     )

    #     self.assertEqual(request.status_code, 200)
    #     data = request.json()
    #     self.assertEqual(data["name"], update["name"])
    #     self.assertEqual(data["side"], str(update["side"]))
    #     self.assertEqual(data["order_size"], update["order_size"])

    # def test_delete_autotrade_object(self):
    #     request = self.client.delete(
    #         reverse("autotrade:MMbotDelete", kwargs={"pk": self.autotrade.id})
    #     )
    #     self.assertEqual(request.status_code, 204)

    # def test_delete_apikey_with_invalid_id(self):
    #     expected_response = {"status": "data not found"}

    #     request = self.client.delete(
    #         reverse("autotrade:MMbotDelete", kwargs={"pk": 922337203685477580})
    #     )
    #     self.assertEqual(request.status_code, 404)
    #     self.assertDictEqual(request.json(), expected_response)

