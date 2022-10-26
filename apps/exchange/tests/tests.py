# from django.test import TestCase

# # Create your tests here.
from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from apps.exchange.tests.factories import *


# Create your tests here.
class TestExchanges(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory.create(password="abc123@", username="testSS")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.exchange = ExchangeFactory.create()

    def test_get_all_exchanges(self):
        data = list(Exchange.objects.filter().values())
        request = self.client.get(reverse("exchange:ExchangeList"))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json()), len(data))


class TestApiKeys(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory.create(password="abc123@", username="testSS")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.exchange = ExchangeFactory.create()

        self.api = ApiKeyFactory.create(
            description="test",
            user=self.user,
            exchange=self.exchange,
        )

    def test_add_apikey(self):
        data = {
            "description": "test",
            "api_key": "DUMMY_KEY",
            "api_secret": "DUMMY_KEY",
            "default": True,
            "user": self.user,
            "exchange": self.exchange.id
        }

        request = self.client.post(reverse("exchange:ApiKeyAdd"), data)
        self.assertEqual(request.status_code, 201)
        response_data = request.json()
        self.assertEqual(response_data.get("exchange"), data["exchange"])
        self.assertEqual(response_data.get("description"), data["description"])
        self.assertEqual(response_data.get("default"), data["default"])

    def test_add_apikey_wth_wrong_parameter(self):
        data = {
            "invalid": "TEST_USDT_FK",
            "api_key": "fake_key000000000000000",
            "api_secret": "fake0000000000000000",
            "description": "i have pain",
            "default": False,
            "exchange": self.exchange.id,
        }

        request = self.client.post(reverse("exchange:ApiKeyAdd"), data)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()["code"], "Invalid data")

    def test_get_all_api_keys(self):
        data = len(ApiKeys.objects.filter(user_id=self.user.id).values())
        request = self.client.get(reverse("exchange:ApiKeyList"))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json()), data)

    def test_detail_apikey(self):
        request = self.client.get(
            reverse("exchange:ApiKeyDetail", kwargs={"pk": self.api.id})
        )
        self.assertEqual(request.status_code, 200)
        data = request.json()

        self.assertEqual(data["description"], self.api.description)
        self.assertEqual(data["default"], self.api.default)
        self.assertEqual(data["id"], self.api.id)

    def test_detail_apikey_with_invalid_id(self):
        request = self.client.get(
            reverse("exchange:ApiKeyDetail", kwargs={"pk": 922337203685477580})
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
            reverse("exchange:ApiKeyUpdate", kwargs={"pk": 922337203685477580}),
            data=update,
        )

        expected_response = {'api_key': '', 'api_secret': '', 'description': '', 'default': False, 'exchange': None,
                             'user': None}

        self.assertEqual(request.status_code, 200)
        self.assertDictEqual(request.json(), expected_response)

    def test_update_apikey(self):
        data = ApiKeys.objects.filter(user_id=self.user.id, id=self.api.id).first()

        update = {
            "description": "i have much more pain",
            "user": self.user.id,
            "api_key": "fake_key1111111111111111",
            "api_secret": "fake0000000000000000",
            "default": False,
            "exchange": self.exchange.id,
        }

        request = self.client.put(
            reverse("exchange:ApiKeyUpdate", kwargs={"pk": data.id}), data=update
        )

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()["api_key"], update["api_key"])
        self.assertEqual(request.json()["api_secret"], str(update["api_secret"]))
        self.assertEqual(request.json()["description"], update["description"])
        self.assertEqual(request.json()["exchange"], update["exchange"])

    def test_delete_apikey(self):
        data = ApiKeys.objects.filter(user_id=self.user.id, id=self.api.id).first()
        request = self.client.delete(
            reverse("exchange:ApiKeyDelete", kwargs={"pk": data.id})
        )
        self.assertEqual(request.status_code, 204)

    def test_delete_apikey_with_invalid_id(self):
        expected_response = {'code': 5,
                             'message': 'Cannot delete a parent row, check foreign key constraint or if the object exist'}

        request = self.client.delete(
            reverse("exchange:ApiKeyDelete", kwargs={"pk": 922337203685477580})
        )
        self.assertEqual(request.status_code, 200)
        self.assertDictEqual(request.json(), expected_response)
