# from django.test import TestCase

# # Create your tests here.
from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from apps.account.tests.factories import UserFactory
from apps.bookfiller.tests.factories import *
from apps.bookfiller.models.models import *
from apps.exchange.tests.factories import *


class TestBookFiller(TestCase):
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
            exchange_id=self.exchange.id,
        )

        self.bookfiller = BookFillerFactory(
            name="TestBookFiller",
            side=2,
            user_id=self.user.id,
            api_key_id=self.api.id,
            pair_token="SCAM",
            order_size=300,
            number_of_orders=20,
            budget=1,
            user_ref_price=0,
            status="STOP",
        )

    def test_add_bookfiller(self):
        data = {
            "name": "TestBookFiller",
            "side": 2,
            "user_id": self.user.id,
            "api_key_id": self.api.id,
            "pair_token": "SCAM",
            "order_size": 300,
            "number_of_orders": 20,
            "budget": 1,
            "user_ref_price": 0,
            "status": "STOP",
        }

        request = self.client.post(reverse("bookfiller:BookFillerAdd"), data)

        print(request.data)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json(), data["description"])
        self.assertEqual(request.json()["api_key"], data["api_key"])
        self.assertEqual(request.json()["user"], data["user"])

    def test_add_bookfiller_wth_wrong_parameter(self):
        data = {
            "invalid": "TEST_USDT_FK",
            "side": 2,
            "user": self.user.id,
            "api_key": self.api.id,
            "pair_token": "SCAM",
            "order_size": 300,
            "number_of_orders": 20,
            "budget": 1,
            "user_ref_price": 0,
            "status": "STOP",
        }

        request = self.client.post(reverse("bookfiller:BookFillerAdd"), data)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()["code"], 2)

    def test_get_all_bookfiller(self):
        data = BookFiller.objects.filter(user_id=self.user.id).values()
        request = self.client.get(reverse("bookfiller:BookFillerList"))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json()), len(data))

    def test_detail_bookfiller(self):
        data = BookFiller.objects.filter(user_id=self.user.id, id=self.bookfiller.id).first()
        request = self.client.get(
            reverse("bookfiller:BookFillerDetail", kwargs={"pk": data.id})
        )

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()[0]["name"], data.name)
        self.assertEqual(request.json()[0]["side"], data.side)
        # self.assertDictEqual(request.json()[0]["order_size"], data["order_size"])
        # self.assertDictEqual(request.json()[0]["status"], data["status"])

    def test_detail_bookfiller_with_invalid_id(self):
        request = self.client.get(
            reverse("bookfiller:BookFillerDetail", kwargs={"pk": 922337203685477580})
        )

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json(), [])

    def test_update_apikey_with_invalid_parameter(self):
        update = {
            "invl": "TEST_USDT_FK",
            "api_key": "fake_key000000000000000",
            "api_secret": "fake0000000000000000",
            "description": "i have pain",
            "default": False,
            "exchange": self.exchange.id,
        }

        request = self.client.put(
            reverse("bookfiller:BookFillerUpdate", kwargs={"pk": 922337203685477580}),
            data=update,
        )

        expected_response = {'api_key': '', 'api_secret': '', 'description': '', 'default': False, 'exchange': None,
                             'user': None}

        self.assertEqual(request.status_code, 200)
        self.assertDictEqual(request.json(), expected_response)

    def test_update_bookfiller(self):
        data = BookFiller.objects.filter(user_id=self.user.id, id=self.api.id).first()

        update = {
            "name": "TestBookFiller Updated",
            "side": 2,
            "user_id": self.user.id,
            "api_key_id": self.api.id,
            "pair_token": "SCAM",
            "order_size": 300,
            "number_of_orders": 20,
            "budget": 1,
            "user_ref_price": 0,
            "status": "STOP",
        }

        request = self.client.put(
            reverse("bookfiller:BookFillerUpdate", kwargs={"pk": data.id}), data=update
        )

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()["name"], update["name"])
        self.assertEqual(request.json()["side"], str(update["side"]))
        self.assertEqual(request.json()["order_size"], update["order_size"])
        self.assertEqual(request.json()["status"], update["status"])


    def test_delete_apikey(self):
        data = BookFiller.objects.filter(user_id=self.user.id, id=self.bookfiller.id).first()
        request = self.client.delete(
            reverse("bookfiller:BookFillerDelete", kwargs={"pk": data.id})
        )
        self.assertEqual(request.status_code, 204)

    def test_delete_apikey_with_invalid_id(self):
        expected_response = {'code': 5,
                             'message': 'Cannot delete a parent row, check foreign key constraint or if the object exist'}

        request = self.client.delete(
            reverse("bookfiller:BookFillerDelete", kwargs={"pk": 922337203685477580})
        )
        self.assertEqual(request.status_code, 200)
        self.assertDictEqual(request.json(), expected_response)

    # def test_bot_status(self):


