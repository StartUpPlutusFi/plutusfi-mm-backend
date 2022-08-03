from logging.config import dictConfig
from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from apps.account.tests.factories import UserFactory
from apps.token.tests.factories import TokenFactory
from apps.dashboard.db.models import BotConfigPairtokens

from django.core.serializers import serialize

import json

# Create your tests here.


class TestToken(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory.create(password="abc123@", username="testSS")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.token = TokenFactory.create(pair="TestUSDT")

    def test_add_token(self):
        data = {
            "pair": "TEST_USDT_FK"
        }

        request = self.client.post(reverse("token:TokenAdd"), data)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()["pair"], "TEST_USDT_FK")
    
    def test_add_token_wth_wrong_parameter(self):
        data = {
            "wrong_name_lmao": "TEST_USDT_FK"
        }

        request = self.client.post(reverse("token:TokenAdd"), data)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()["code"], 2)

    def test_get_all_tokens(self):

        data =  list(BotConfigPairtokens.objects.all().values())
        request = self.client.get(reverse("token:TokenList"))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json()), len(data))

    def test_detail_token(self):

        data =  BotConfigPairtokens.objects.first()
        request = self.client.get(reverse("token:TokenDetail", kwargs={"pk": data.id }))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()[0]['id'], data.id )
        self.assertEqual(request.json()[0]['pair'], data.pair )

    def test_update_token(self):

        data =  BotConfigPairtokens.objects.first()
        
        update = {
            "pair": "UpdatedToken",
        }

        request = self.client.put(reverse("token:TokenUpdate", kwargs={"pk": data.id }), data=update)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()['pair'], "UpdatedToken" )

    def test_delete_token(self):

        data =  BotConfigPairtokens.objects.first()
        request = self.client.delete(reverse("token:TokenDelete", kwargs={"pk": data.id }))
        self.assertEqual(request.status_code, 204)
    
    def test_delete_token_with_invalid_id(self):

        request = self.client.delete(reverse("token:TokenDelete", kwargs={"pk": 99999999999999999999999999 }))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()['code'], 5 )