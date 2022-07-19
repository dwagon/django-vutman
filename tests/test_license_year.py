from django.test import TestCase
import os
import datetime


class SimpleTestCase(TestCase):
    def test_license_year(self):
        self.assertEqual(os.path.exists("LICENSE"), True)
        now = datetime.datetime.now()
        current_year = datetime.datetime.strftime(now, "%Y")
        license_text = open("LICENSE").read()
        expected_text = "Copyright (c) %s Daniel Lawrence" % current_year
        self.assertIn(expected_text, license_text)
