# from django.test import TestCase

# # Create your tests here.
from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from apps.account.tests.factories import UserFactory
from apps.exchange_api.tests.factories import ExchangeFactory
from apps.token.tests.factories import TokenFactory
from apps.dashboard.db.models import Exchange

# Create your tests here.
class Testexchanges(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory.create(password="abc123@", username="testSS")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.exchange = ExchangeFactory(
            name = "ScamEx"
        )

    def test_add_exchange(self):
        data = {
            "name": "ScamEx"
        }

        request = self.client.post(reverse("exchange:ExchangeAdd"), data)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()['name'], data['name'])
    
    def test_add_exchange_wth_wrong_parameter(self):
        data = {
            "wrong_name_lmao": "fake_ex",
           
        }

        request = self.client.post(reverse("exchange:ExchangeAdd"), data)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()["code"], 2)

    def test_get_all_exchanges(self):

        data =  list(Exchange.objects.all().values())
        request = self.client.get(reverse("exchange:ExchangeList"))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json()), len(data))

    def test_detail_exchange(self):

        data =  Exchange.objects.first()
        request = self.client.get(reverse("exchange:ExchangeDetail", kwargs={"pk": data.id }))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()[0]['name'], data.name )

    def test_update_exchange(self):

        data =  Exchange.objects.first()
        
        update = {
            "name": "NewScamExLmao"
        }

        request = self.client.put(reverse("exchange:ExchangeUpdate", kwargs={"pk": data.id }), data=update)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()['name'], update['name'] )

    def test_delete_exchange(self):

        data =  Exchange.objects.first()
        request = self.client.delete(reverse("exchange:ExchangeDelete", kwargs={"pk": data.id }))
        self.assertEqual(request.status_code, 204)
    
    def test_delete_exchange_with_invalid_id(self):

        request = self.client.delete(reverse("exchange:ExchangeDelete", kwargs={"pk": 922337203685477580 }))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()['code'], 5 )