from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from apps.autotrade.tests.factories import *
from apps.exchange.tests.factories import *


import io
from PIL import Image


class TestAutoTrade(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory.create(password="abc123@", username="testSS")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.exchange = ExchangeFactory.create()

        self.apikey = ApiKeyFactory.create(
            description="test",
            user=self.user,
            exchange=self.exchange,
        )

        self.autotrade = MMFactory.create(
            name="Test Autotrade",
            description="Generic",
            user=self.user,
            api_key=self.apikey,
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
            "api_key_id": self.apikey.id,
            "pair_token": "TESTDUMMY",
            "user_ref_price": 100,
            "side": 1,
            "trade_candle": 10,
            "trade_amount": 100.99,
            "status": "STOP",
        }

        request = self.client.post(reverse("MMbot:MMbotAdd"), data)

        self.assertEqual(request.status_code, 201)
        request_data = request.json()

        self.assertIsNotNone(request.json()["photo"])
        self.assertEqual(request_data["name"], data["name"])
        self.assertEqual(request_data["description"], data["description"])
        self.assertEqual(request_data["api_key"], data["api_key_id"])
        self.assertEqual(request_data["pair_token"], data["pair_token"])
        self.assertEqual(request_data["user_ref_price"], data["user_ref_price"])
        self.assertEqual(request_data["side"], data["side"])
        self.assertEqual(request_data["trade_candle"], data["trade_candle"])
        self.assertEqual(request_data["trade_amount"], data["trade_amount"])
        self.assertEqual(request_data["status"], data["status"])

    def test_add_autotrade_with_invalid_file(self):
        data = {
            "photo": b"0x00000000",
            "name": b"0x00000000",
            "description": b"0x00000000",
            "user": b"0x00000000",
            "api_key_id": b"0x00000000",
            "pair_token": b"0x00000000",
            "user_ref_price": b"0x00000000",
            "side": b"0x00000000",
            "trade_candle": b"0x00000000",
            "trade_amount": b"0x00000000",
            "status": b"0x00000000",
        }

        request = self.client.post(reverse("MMbot:MMbotAdd"), data)
        expected = {
            "photo": [
                "The submitted data was not a file. Check the encoding type on the form."
            ]
        }

        self.assertEqual(request.status_code, 400)
        self.assertDictEqual(request.json(), expected)

    def test_add_autotrade_with_invalid_data_and_null_file(self):
        data = {
            "photo": "",
            "name": "0x00000000",
            "description": "0x00000000",
            "user": "0x00000000",
            "api_key_id": "0x00000000",
            "pair_token": "0x00000000",
            "user_ref_price": "0x00000000",
            "side": "0x00000000",
            "trade_candle": "0x00000000",
            "trade_amount": "0x00000000",
            "status": "0x00000000",
        }

        request = self.client.post(reverse("MMbot:MMbotAdd"), data)

        self.assertEqual(request.status_code, 400)
        request_data = request.json()
        expected = {
            "api_key_id": ["A valid integer is required."],
            "side": ["A valid integer is required."],
            "user_ref_price": ["A valid number is required."],
            "trade_candle": ["A valid integer is required."],
            "trade_amount": ["A valid number is required."],
        }
        self.assertDictEqual(request_data, expected)

    def test_get_all_autotrade(self):
        data = MarketMakerBot.objects.filter(user_id=self.user.id).values()
        request = self.client.get(reverse("MMbot:MMbotList"))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json()), len(data))

    def test_detail_autotrade(self):

        data = (
            MarketMakerBot.objects.filter(user_id=self.user.id, id=self.autotrade.id)
            .values()
            .first()
        )

        request = self.client.get(
            reverse("MMbot:MMbotDetail", kwargs={"pk": data["id"]})
        )

        self.assertEqual(request.status_code, 200)
        request_data = request.json()[0]

        self.assertEqual(request_data["name"], data["name"])
        self.assertEqual(request_data["description"], data["description"])
        self.assertEqual(request_data["api_key"], data["api_key_id"])
        self.assertEqual(request_data["pair_token"], data["pair_token"])
        self.assertEqual(request_data["user_ref_price"], data["user_ref_price"])
        self.assertEqual(request_data["side"], data["side"])
        self.assertEqual(request_data["trade_candle"], data["trade_candle"])
        self.assertEqual(request_data["trade_amount"], data["trade_amount"])
        self.assertEqual(request_data["status"], data["status"])

    def test_detail_autotrade_with_invalid_id(self):
        request = self.client.get(
            reverse("MMbot:MMbotDetail", kwargs={"pk": 922337203685477580})
        )

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json(), [])

    def test_update_autotrade(self):
        update = {
            "photo": self.gen_image(color=(45, 45, 45)),
            "name": "Test Autotrade",
            "description": "Generic Updated",
            "user": self.user,
            "pair_token": "TESTDUMMY",
            "user_ref_price": 999,
            "side": 2,
            "trade_candle": 15,
            "trade_amount": 100.99,
        }

        request = self.client.put(
            reverse("MMbot:MMbotUpdate", kwargs={"pk": self.autotrade.id}),
            data=update,
        )

        request_data = request.json()

        self.assertEqual(request.status_code, 200)
        self.assertIsNotNone(request.json()["photo"])
        self.assertEqual(request_data["name"], update["name"])
        self.assertEqual(request_data["description"], update["description"])
        self.assertEqual(request_data["pair_token"], update["pair_token"])
        self.assertEqual(request_data["user_ref_price"], update["user_ref_price"])
        self.assertEqual(request_data["side"], update["side"])
        self.assertEqual(request_data["trade_candle"], update["trade_candle"])
        self.assertEqual(request_data["trade_amount"], update["trade_amount"])

    def test_delete_autotrade(self):

        data = MarketMakerBot.objects.filter(
            user_id=self.user.id, id=self.autotrade.id
        ).first()

        request = self.client.delete(
            reverse("MMbot:MMbotDelete", kwargs={"pk": data.id})
        )

        expected = {"status": "done"}

        self.assertEqual(request.status_code, 200)
        request_data = request.json()
        self.assertDictEqual(request_data, expected)
