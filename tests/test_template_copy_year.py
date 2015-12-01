from django.test import TestCase
import os
import datetime


class SimpleTestCase(TestCase):

    def test_license_year(self):
        BASE_TEMPLATE = "./vutman/templates/base.html"
        self.assertEqual(os.path.exists(BASE_TEMPLATE), True)
        now = datetime.datetime.now()
        current_year = datetime.datetime.strftime(now, '%Y')
        license_text = open(BASE_TEMPLATE).read()
        expected_text = 'Copyright \xc2\xa9 {0}'.format(current_year)
        self.assertIn(expected_text, license_text)
