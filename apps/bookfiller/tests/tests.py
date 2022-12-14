# from django.test import TestCase

# # Create your tests here.
from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from apps.bookfiller.tests.factories import *
from apps.exchange.tests.factories import *


class TestBookFiller(TestCase):
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

        self.bookfiller = BookFillerFactory.create(
            name="TestBookFiller",
            side=2,
            user=self.user,
            api_key=self.apikey,
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
            "api_key_id": self.apikey.id,
            "pair_token": "SCAM",
            "order_size": 300,
            "number_of_orders": 20,
            "budget": 1,
            "user_ref_price": 110,
        }

        request = self.client.post(reverse("bookfiller:BookFillerAdd"), data)

        self.assertEqual(request.status_code, 201)

    def test_add_bookfiller_wth_wrong_parameter(self):
        data = {
            "invalid": "TEST_USDT_FK",
            "side": 2,
            "user": self.user.id,
            "api_key_id": self.apikey.id,
            "pair_token": "SCAM",
            "order_size": 300,
            "number_of_orders": 20,
            "budget": 1,
            "user_ref_price": 0,
            "status": "STOP",
        }

        request = self.client.post(reverse("bookfiller:BookFillerAdd"), data)

        self.assertEqual(request.status_code, 400)
        data = request.json()

        self.assertEqual(*data.get("name"), "This field is required.")

    def test_get_all_bookfiller(self):
        data = BookFiller.objects.filter(user_id=self.user.id).values()
        request = self.client.get(reverse("bookfiller:BookFillerList"))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json()), len(data))

    def test_detail_bookfiller(self):
        data = BookFiller.objects.filter(
            user_id=self.user.id, id=self.bookfiller.id
        ).first()
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

    def test_update_bookfiller_with_invalid_parameter(self):
        update = {
            "name": "TestBookFiller",
            "side": 400,
            "api_key_id": "www67",
            "pair_token": "SCAM",
            "order_size": 300,
            "budget": 1,
            "user_ref_price": "110"
        }

        request = self.client.put(
            reverse("bookfiller:BookFillerUpdate", kwargs={"pk": 922337203685477580}),
            data=update,
        )

        expected_response = {
            "error": True,
            "errors": {
                "api_key_id": "A valid integer is required.",
                "number_of_orders": "This field is required."
            }
        }

        self.assertEqual(request.status_code, 500)
        data = request.json()

        self.assertDictEqual(data, expected_response)

    def test_update_bookfiller(self):
        update = {
            "name": "TestBookFiller Updated",
            "side": 2,
            "user_id": self.user.id,
            "api_key_id": self.apikey.id,
            "pair_token": "SCAM",
            "order_size": 300,
            "number_of_orders": 20,
            "budget": 1,
            "user_ref_price": 0,
            "status": "STOP",
        }

        request = self.client.put(
            reverse("bookfiller:BookFillerUpdate", kwargs={"pk": self.bookfiller.id}),
            data=update,
        )

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()["name"], update["name"])
        self.assertEqual(request.json()["side"], str(update["side"]))
        self.assertEqual(request.json()["order_size"], update["order_size"])

    def test_delete_apikey(self):
        data = BookFiller.objects.filter(
            user_id=self.user.id, id=self.bookfiller.id
        ).first()
        request = self.client.delete(
            reverse("bookfiller:BookFillerDelete", kwargs={"pk": data.id})
        )
        self.assertEqual(request.status_code, 204)

    def test_delete_apikey_with_invalid_id(self):
        expected_response = {"status": "data not found"}

        request = self.client.delete(
            reverse("bookfiller:BookFillerDelete", kwargs={"pk": 922337203685477580})
        )
        self.assertEqual(request.status_code, 404)
        data = request.json()
        self.assertDictEqual(data, expected_response)

    def test_return_bookfiller_cancel_code(self):
        request = self.client.get(
            reverse("bookfiller:BookFillerCancelCode", kwargs={"pk": 922337203685477580})
        )

        self.assertEqual(request.status_code, 200)
        data = request.json()
        self.assertEqual(request.json(), [])
        self.assertEqual(isinstance(request.json(), list), isinstance([], list))
