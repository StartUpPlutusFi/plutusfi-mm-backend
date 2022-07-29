from django.test import TestCase

from .factories import UserFactory


# Create your tests here.
class TestAccountFunctionalities(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory()

    def test_user_was_created(self):
        self.assertTrue(self.user)

    def test_user_has_name(self):
        self.assertIsNotNone(self.user.username)

    def test_user_has_password(self):
        self.assertIsNotNone(self.user.password)

    def test_user_has_email(self):
        self.assertIsNotNone(self.user.email)

    def test_user_has_first_and_last_name(self):
        self.assertIsNotNone(self.user.first_name)
        self.assertIsNotNone(self.user.last_name)

    def test_user_has_profile(self):
        self.assertIsNotNone(self.user.profile)
        print("profile", self.user.profile)
