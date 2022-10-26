from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from apps.bookfiller.tests.factories import *
from apps.exchange.tests.factories import *


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

        self.bookfiller = BookFillerFactory.create(
            name="TestBookFiller",
            side=2,
            user_id=self.user.id,
            api_key_id=self.API.id,
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
            "user": self.user.id,
            "api_key_id": self.API.id,
            "pair_token": "SCAM",
            "order_size": 300,
            "number_of_orders": 20,
            "budget": 1,
            "user_ref_price": 0,
            "status": "STOP",
        }

        request = self.client.post(reverse("bookfiller:BookFillerAdd"), data)

        self.assertEqual(request.status_code, 201)
        request_data = request.json()

        self.assertEqual(request_data["name"], data["name"])
        self.assertEqual(request_data["user"], data["user"])

    def test_add_bookfiller_wth_wrong_parameter(self):
        data = {
            "invalid": "TEST_USDT_FK",
            "side": 2,
            "user": self.user.id,
            "api_key_id": self.API.id,
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
        data = BookFiller.objects.filter(user_id=self.user.id, id=self.bookfiller.id).first()
        request = self.client.get(
            reverse("bookfiller:BookFillerDetail", kwargs={"pk": data.id})
        )

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()[0]["name"], data.name)
        self.assertEqual(request.json()[0]["side"], data.side)

    def test_detail_bookfiller_with_invalid_id(self):
        request = self.client.get(
            reverse("bookfiller:BookFillerDetail", kwargs={"pk": 922337203685477580})
        )

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json(), [])

    def test_update_bookfiller_with_invalid_parameter(self):
        update = {
            "invl": "TEST_USDT_FK",
            "api_key": "fake_key000000000000000",
            "api_secret": "fake0000000000000000",
            "description": "i have pain",
            "default": False,
            "exchange": self.exchange.id,
        }

        response = self.client.put(
            reverse("bookfiller:BookFillerUpdate", kwargs={"pk": 922337203685477580}),
            data=update,
        )

        self.assertEqual(response.status_code, 500)
        data = response.json()

        expected_response = {'error': True,
                             'errors': {'name': 'This field is required.', 'side': 'This field is required.',
                                        'user_id': 'This field is required.', 'order_size': 'This field is required.',
                                        'api_key_id': 'This field is required.',
                                        'pair_token': 'This field is required.',
                                        'number_of_orders': 'This field is required.',
                                        'budget': 'This field is required.',
                                        'user_ref_price': 'This field is required.'}}

        self.assertDictEqual(data, expected_response)

    def test_update_bookfiller(self):
        update = {
            "name": "TestBookFiller Updated",
            "side": 2,
            "user_id": self.user.id,
            "api_key_id": self.API.id,
            "pair_token": "SCAM",
            "order_size": 300,
            "number_of_orders": 20,
            "budget": 1,
            "user_ref_price": 0,
            "status": "STOP",
        }

        request = self.client.put(
            reverse("bookfiller:BookFillerUpdate", kwargs={"pk": self.bookfiller.id}), data=update
        )

        self.assertEqual(request.status_code, 200)
        data = request.json()
        self.assertEqual(data["name"], update["name"])
        self.assertEqual(data["side"], str(update["side"]))
        self.assertEqual(data["order_size"], update["order_size"])

    def test_delete_bookfiller_object(self):
        request = self.client.delete(
            reverse("bookfiller:BookFillerDelete", kwargs={"pk": self.bookfiller.id})
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
