# from django.test import TestCase

# # Create your tests here.
from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from apps.account.tests.factories import UserFactory
from apps.exchange_api.tests.factories import ApiKeyFactory, ExchangeFactory
from apps.token.tests.factories import TokenFactory
from apps.dashboard.db.models import ApiKeys

# Create your tests here.
class TestApiKeys(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory.create(password="abc123@", username="testSS")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.exchange = ExchangeFactory(
            name = "ScamEx"
        )

        self.api = ApiKeyFactory.create(
            description = "test",
            user = self.user,
            api_key = "0x0000000000",
            api_secret = "0x11111111",
            default = False,
            exchange = self.exchange
        )

    def test_add_apikey(self):
        data = {
            "description":"i have pain",
            "api_key": "fake_key000000000000000",
            "api_secret": "fake0000000000000000",
            "default": False,
            "exchange": self.exchange.id

        }

        request = self.client.post(reverse("apikey:ApiKeyAdd"), data)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json(), data['description'])
        self.assertEqual(request.json()['api_key'], data['api_key'])
        self.assertEqual(request.json()['user'], data['user'])
    
    def test_add_apikey_wth_wrong_parameter(self):
        data = {
            "wrong_name_lmao": "TEST_USDT_FK",
            "api_key" : "fake_key000000000000000",
            "api_secret" : "fake0000000000000000",
            "description" : "i have pain",
            "default" : False,
            "exchange" : self.exchange.id
        }

        request = self.client.post(reverse("apikey:ApiKeyAdd"), data)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()["code"], 2)

    def test_get_all_apikeys(self):

        data =  list(ApiKeys.objects.all().values())
        request = self.client.get(reverse("apikey:ApiKeyList"))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json()), len(data))

    def test_detail_apikey(self):

        data =  ApiKeys.objects.first()
        request = self.client.get(reverse("apikey:ApiKeyDetail", kwargs={"pk": data.id }))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()[0]['description'], data.description)
        self.assertEqual(request.json()[0]['api_key'], data.api_key)
        self.assertEqual(request.json()[0]['user'], data.user.id)
    
    def test_detail_apikey_with_invalid_id(self):

        request = self.client.get(reverse("apikey:ApiKeyDetail", kwargs={"pk": 922337203685477580 }))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json(), [] )

    def test_update_apikey_with_invalid_paramter(self):

        update = {
            "clover_fake": "Nwe scam test",
        }

        request = self.client.put(reverse("apikey:ApiKeyUpdate", kwargs={"pk": 922337203685477580 }), data=update)
        self.assertEqual(request.status_code, 200)
        self.assertIsNot(request.json(), [])

    def test_update_apikey(self):

        data =  ApiKeys.objects.first()
        
        update = {
            "description" : "i have much more pain",
            "user" : self.user.id,
            "api_key" : "fake_key1111111111111111",
            "api_secret" : "fake0000000000000000",
            "default" : False,
            "exchange" : self.exchange.id
        }

        request = self.client.put(reverse("apikey:ApiKeyUpdate", kwargs={"pk": data.id }), data=update)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()['api_key'], update['api_key'] )
        self.assertEqual(request.json()['description'], update['description'] )

    def test_delete_apikey(self):

        data =  ApiKeys.objects.first()
        request = self.client.delete(reverse("apikey:ApiKeyDelete", kwargs={"pk": data.id }))
        self.assertEqual(request.status_code, 204)
    
    def test_delete_apikey_with_invalid_id(self):

        request = self.client.delete(reverse("apikey:ApiKeyDelete", kwargs={"pk": 922337203685477580 }))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()['code'], 5 )