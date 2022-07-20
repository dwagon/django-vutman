""" Testing template """
import os
import datetime
from django.test import TestCase


class SimpleTestCase(TestCase):
    def test_license_year(self):
        BASE_TEMPLATE = "./vutman/templates/base.html"
        self.assertEqual(os.path.exists(BASE_TEMPLATE), True)
        now = datetime.datetime.now()
        current_year = datetime.datetime.strftime(now, "%Y")
        license_text = open(BASE_TEMPLATE).read()
        expected_text = f"Copyright © {current_year}"
        self.assertIn(expected_text, license_text)
