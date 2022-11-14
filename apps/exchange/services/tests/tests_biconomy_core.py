from django.test import TestCase
from apps.exchange.services.biconomy.biconomy_core import *


class TestBiconomyCore(TestCase):
    def test_static_function_encrypt_string(self):

        testString = "536788F4DBDFFEECFBB8F350A941EEA3"
        cavalo = "C965492A50B519451BE98427EA60397B"
        self.assertEqual(encript_string("testString"), testString)
        self.assertEqual(encript_string("cavalo"), cavalo)
