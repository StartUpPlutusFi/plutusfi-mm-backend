from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from apps.account.tests.factories import UserFactory


# Create your tests here.


class TestAuthSystem(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory.create(password="abc123@", username="testA")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_register_user(self):
        data = {
            "username": "test",
            "email": "test@mail.com",
            "password1": "abc123@",
            "password2": "abc123@",
        }
        client = APIClient()
        request = client.post(reverse("auth:register"), data=data)

        self.assertEqual(request.status_code, 201)
        self.assertEqual(request.json()["username"], "test")
        self.assertEqual(request.json()["email"], "test@mail.com")
        self.assertIsNotNone(request.json()["id"])
        self.assertIsNotNone(request.json()["refresh"])
        self.assertIsNotNone(request.json()["access"])

    def test_login(self):
        data = {
            "username": "test",
            "email": "test@mail.com",
            "password1": "abc123@",
            "password2": "abc123@",
        }
        client = APIClient()
        request = client.post(reverse("auth:register"), data=data)

        self.assertEqual(request.status_code, 201)

        data = {"username": data["username"], "password": data["password1"]}

        client = APIClient()
        request = client.post(reverse("auth:login"), data=data)
        self.assertEqual(request.status_code, 200)
        self.assertIsNotNone(request.json()["refresh"])
        self.assertIsNotNone(request.json()["access"])

    def test_login_invalid_credentials(self):
        data = {
            "username": "test",
            "email": "test@mail.com",
            "password1": "abc123@",
            "password2": "abc123@",
        }
        client = APIClient()
        request = client.post(reverse("auth:register"), data=data)

        self.assertEqual(request.status_code, 201)

        data = {"username": data["username"], "password": "invalid-password"}

        client = APIClient()
        request = client.post(reverse("auth:login"), data=data)
        self.assertEqual(request.status_code, 401)
        self.assertEqual(
            request.json()["detail"],
            "No active account found with the given credentials",
        )

    def test_no_send_username_in_data(self):
        data = {
            "username": "test",
            "email": "test@mail.com",
            "password1": "abc123@",
            "password2": "abc123@",
        }
        client = APIClient()
        request = client.post(reverse("auth:register"), data=data)

        self.assertEqual(request.status_code, 201)

        data = {"password": "invalid-password"}

        client = APIClient()
        request = client.post(reverse("auth:login"), data=data)
        self.assertEqual(request.status_code, 400)
        self.assertEqual(request.json()["username"], ['This field is required.'])
