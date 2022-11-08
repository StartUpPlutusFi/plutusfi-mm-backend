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
