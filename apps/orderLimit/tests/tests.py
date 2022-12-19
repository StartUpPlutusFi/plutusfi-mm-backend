from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from apps.orderLimit.tests.factories import *
from apps.exchange.tests.factories import *


class TestOrderLimit(TestCase):
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

        self.orderLimit = OrderLimitFactory.create(
            name="TestOrderLimit",
            side=2,
            user=self.user,
            api_key_id=self.apikey.id,
            pair_token="TEST_USDT",
            quantity=10000,
            price=0.01,
            status="STOP",
        )

    def test_add_orderLimit(self):
        data = {
            "name": "TestOrderLimit",
            "side": 2,
            "user": self.user,
            "api_key_id": self.apikey.id,
            "pair_token": "TEST_USDT",
            "quantity": 10000,
            "price": 0.01,
        }

        request = self.client.post(reverse("orderLimit:OrderLimitAdd"), data)

        response = request.json()
        self.assertEqual(request.status_code, 201)
        self.assertEqual(response["name"], data["name"])
        self.assertEqual(response["side"], str(data["side"]))
        self.assertEqual(response["price"], data["price"])
        self.assertEqual(response["quantity"], data["quantity"])

    def test_add_orderLimit_wth_wrong_parameter(self):
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

        request = self.client.post(reverse("orderLimit:OrderLimitAdd"), data)

        self.assertEqual(request.status_code, 400)
        data = request.json()

        self.assertEqual(*data.get("name"), "This field is required.")

    def test_get_all_orderLimit(self):
        data = OrderLimit.objects.filter(user_id=self.user.id).values()
        request = self.client.get(reverse("orderLimit:OrderLimitList"))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json()), len(data))

    def test_detail_orderLimit(self):
        data = OrderLimit.objects.filter(
            user_id=self.user.id, id=self.orderLimit.id
        ).first()
        request = self.client.get(
            reverse("orderLimit:OrderLimitDetail", kwargs={"pk": data.id})
        )

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()[0]["name"], data.name)
        self.assertEqual(request.json()[0]["side"], data.side)

    def test_detail_orderLimit_with_invalid_id(self):
        request = self.client.get(
            reverse("orderLimit:OrderLimitDetail", kwargs={"pk": 922337203685477580})
        )

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json(), [])

    def test_update_orderLimit_with_invalid_parameter(self):
        update = {
            "name": "TestOrderLimit",
            "side": 400,
            "api_key_id": "www67",
            "pair_token": "SCAM",
            "order_size": 300,
            "budget": 1,
            "user_ref_price": "110",
        }

        request = self.client.put(
            reverse("orderLimit:OrderLimitUpdate", kwargs={"pk": 922337203685477580}),
            data=update,
        )

        expected_response = {
            "error": True,
            "errors": {
                "api_key_id": "A valid integer is required.",
                "quantity": "This field is required.",
                "price": "This field is required.",
            },
        }
        data = request.json()

        self.assertEqual(request.status_code, 500)
        self.assertDictEqual(data, expected_response)

    def test_update_orderLimit(self):
        update = {
            "name": "UpdatedOrderLimit",
            "side": 2,
            "user": self.user,
            "api_key_id": self.apikey.id,
            "pair_token": "TEST_USDT",
            "quantity": 10000,
            "price": 0.01,
        }

        request = self.client.put(
            reverse("orderLimit:OrderLimitUpdate", kwargs={"pk": self.orderLimit.id}),
            data=update,
        )

        data = request.json()

        self.assertEqual(request.status_code, 200)
        self.assertEqual(data["name"], update["name"])
        self.assertEqual(data["side"], str(update["side"]))
        self.assertEqual(data["price"], update["price"])

    def test_delete_apikey(self):
        data = OrderLimit.objects.filter(
            user_id=self.user.id, id=self.orderLimit.id
        ).first()
        request = self.client.delete(
            reverse("orderLimit:OrderLimitDelete", kwargs={"pk": data.id})
        )
        self.assertEqual(request.status_code, 204)

    def test_delete_apikey_with_invalid_id(self):
        expected_response = {"status": "data not found"}

        request = self.client.delete(
            reverse("orderLimit:OrderLimitDelete", kwargs={"pk": 922337203685477580})
        )
        self.assertEqual(request.status_code, 404)
        data = request.json()
        self.assertDictEqual(data, expected_response)
