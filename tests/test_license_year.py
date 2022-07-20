from django.test import TestCase
import os
import datetime


class SimpleTestCase(TestCase):
    def test_license_year(self):
        self.assertEqual(os.path.exists("LICENSE"), True)
        now = datetime.datetime.now()
        current_year = datetime.datetime.strftime(now, "%Y")
        license_text = open("LICENSE").read()
        expected_text = f"Copyright (c) {current_year} Daniel Lawrence"
        self.assertIn(expected_text, license_text)
