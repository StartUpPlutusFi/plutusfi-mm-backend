# from django.test import TestCase

# # Create your tests here.
from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from apps.account.tests.factories import UserFactory
from apps.exchange.tests.factories import *
from apps.exchange.models.models import Exchange, ApiKeys


# Create your tests here.
class TestExchanges(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory.create(password="abc123@", username="testSS")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.exchange = ExchangeFactory(name="ScamEx")

    def test_add_exchange(self):

        data = {"name": "ScamEx"}
        request = self.client.post(reverse("exchange:ExchangeAdd"), data)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()["name"], data["name"])

    def test_add_exchange_wth_wrong_parameter(self):
        data = {
            "invalid_field": "fake_ex",
        }

        request = self.client.post(reverse("exchange:ExchangeAdd"), data)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()["code"], 2)

    def test_get_all_exchanges(self):
        data = list(Exchange.objects.filter().values())
        request = self.client.get(reverse("exchange:ExchangeList"))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json()), len(data))

    def test_detail_exchange(self):
        data = Exchange.objects.filter(id=self.exchange.id).first()
        request = self.client.get(
            reverse("exchange:ExchangeDetail", kwargs={"pk": data.id})
        )
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()[0]["name"], data.name)

    def test_detail_exchange_with_invalid_id(self):
        request = self.client.get(
            reverse("exchange:ExchangeDetail", kwargs={"pk": 922337203685477580})
        )
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json(), [])

    def test_update_exchange_with_invalid_paramter(self):
        update = {
            "clover_fake": "New scam ex",
        }

        request = self.client.put(
            reverse("exchange:ExchangeUpdate", kwargs={"pk": 922337203685477580}),
            data=update,
        )
        self.assertEqual(request.status_code, 200)
        self.assertIsNot(request.json(), [])

    def test_update_exchange(self):
        data = Exchange.objects.filter(id=self.exchange.id).first()

        update = {"name": "NewScamExLmao"}

        request = self.client.put(
            reverse("exchange:ExchangeUpdate", kwargs={"pk": data.id}), data=update
        )
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()["name"], update["name"])

    def test_delete_exchange(self):
        data = Exchange.objects.filter(id=self.exchange.id).first()
        request = self.client.delete(
            reverse("exchange:ExchangeDelete", kwargs={"pk": data.id})
        )
        self.assertEqual(request.status_code, 204)

    def test_delete_exchange_with_invalid_id(self):
        request = self.client.delete(
            reverse("exchange:ExchangeDelete", kwargs={"pk": 922337203685477580})
        )
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()["code"], 5)


class TestApiKeys(TestCase):
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

    def test_add_apikey(self):
        data = {
            "description": "test",
            "api_key": "fake_key000000000000000",
            "api_secret": "fake0000000000000000",
            "default": False,
            "exchange_id": self.exchange.id,
        }

        request = self.client.post(reverse("exchange:ApiKeyAdd"), data)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json(), data["description"])
        self.assertEqual(request.json()["api_key"], data["api_key"])
        self.assertEqual(request.json()["user"], data["user"])

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
        self.assertEqual(request.json()["code"], 2)

    def test_get_all_api_keys(self):

        data = len(ApiKeys.objects.filter(user_id=self.user.id).values())
        request = self.client.get(reverse("exchange:ApiKeyList"))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json()), data)

    def test_detail_apikey(self):

        data = ApiKeys.objects.filter(user_id=self.user.id, id=self.api.id).first()
        request = self.client.get(
            reverse("exchange:ApiKeyDetail", kwargs={"pk": data.id})
        )
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()[0]["description"], data.description)
        self.assertEqual(request.json()[0]["api_key"], data.api_key)
        self.assertEqual(request.json()[0]["user"], data.user.id)

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

        expected_response = {'api_key': '', 'api_secret': '', 'description': '', 'default': False, 'exchange': None, 'user': None}

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

        expected_response = {'id': 8, 'api_key': 'fake_key1111111111111111', 'api_secret': 'fake0000000000000000', 'description': 'i have much more pain', 'default': False, 'exchange': 8, 'user': 8}

        self.assertEqual(request.status_code, 200)
        self.assertDictEqual(request.json(), expected_response)

    def test_delete_apikey(self):

        data = ApiKeys.objects.filter(user_id=self.user.id, id=self.api.id).first()
        request = self.client.delete(
            reverse("exchange:ApiKeyDelete", kwargs={"pk": data.id})
        )
        self.assertEqual(request.status_code, 204)

    def test_delete_apikey_with_invalid_id(self):

        expected_response = {'code': 5, 'message': 'Cannot delete a parent row, check foreign key constraint or if the object exist'}

        request = self.client.delete(
            reverse("exchange:ApiKeyDelete", kwargs={"pk": 922337203685477580})
        )
        self.assertEqual(request.status_code, 200)
        self.assertDictEqual(request.json(), expected_response)
