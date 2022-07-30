import io

from PIL import Image
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

    @staticmethod
    def gen_image(color=(255, 255, 255)):
        file = io.BytesIO()
        image = Image.new("RGBA", size=(100, 100), color=color)
        image.save(file, "png")
        file.name = "test.png"
        file.seek(0)
        return file

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
        self.assertEqual(request.json()["username"], ["This field is required."])

    def test_get_profile_user(self):
        request = self.client.get(reverse("auth:profile"))
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()["id"], self.user.profile.id)
        self.assertEqual(request.json()["user"]["username"], self.user.username)
        self.assertEqual(request.json()["user"]["first_name"], self.user.first_name)
        self.assertEqual(request.json()["user"]["last_name"], self.user.last_name)
        self.assertEqual(request.json()["user"]["email"], self.user.email)

    def test_update_profile(self):
        data = {
            "last_name": "test",
            "picture": self.gen_image()
        }

        request = self.client.put(reverse("auth:profile-update"), data=data)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()["user"]["last_name"], data["last_name"])
        self.assertIsNotNone(request.json()["picture"])
