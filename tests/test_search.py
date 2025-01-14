from django.test import TestCase
from vutman.models import EmailAlias, EmailUser, EmailDomain, EmailServer
from vutman.search_indexes import (
    make_search_query,
    search_emailaliases,
    search_emailuser,
    search_from_request,
)
from collections import namedtuple


class SimpleTestCase(TestCase):
    def setUp(self):
        self.server = EmailServer.objects.create(email_server="server")
        self.domain = EmailDomain.objects.create(domain_name="domain")
        self.user = EmailUser.objects.create(
            username="username",
            fullname="first last",
            email_server=self.server,
            active_directory_basedn="basedn",
        )
        self.alias = EmailAlias.objects.create(
            alias_name="alias", username=self.user, email_domain=self.domain
        )

    def test_make_search_query(self):
        query = make_search_query("term", ["fieldname"])
        self.assertEqual(str(query), "(AND: ('fieldname__icontains', 'term'))")

        query = make_search_query("term", ["field1", "field2"])
        self.assertIn("OR", str(query))
        self.assertIn("field1__icontains", str(query))
        self.assertIn("field2__icontains", str(query))
        self.assertIn("term", str(query))

    def test_make_search_query_many_terms(self):
        query = make_search_query("term", ["field1", "field2", "field3", "field4"])
        self.assertIn("OR", str(query))
        self.assertIn("field1__icontains", str(query))
        self.assertIn("field2__icontains", str(query))
        self.assertIn("field3__icontains", str(query))
        self.assertIn("field4__icontains", str(query))
        self.assertIn("term", str(query))

    def test_basic_search_alias(self):
        expected_results = [
            ("Alias", 1),
            ("username", 1),
            ("name", 1),
            ("user", 1),
            ("basedn", 1),
            ("domain", 1),
            ("USErname", 1),
            ("naMe", 1),
            ("uSEr", 1),
            ("baSEDn", 1),
            ("domAIn", 1),
            ("server", 1),
            ("SERVer", 1),
            #
            ("bad_username", 0),
            ("ZZZ", 0),
            ("1", 0),
        ]

        for term, count in expected_results:
            results = search_emailaliases(term)
            self.assertEqual(len(results), count)

    def test_basic_search_user(self):
        expected_results = [
            ("username", 1),
            ("name", 1),
            ("user", 1),
            ("basedn", 1),
            ("USErname", 1),
            ("naMe", 1),
            ("uSEr", 1),
            ("baSEDn", 1),
            ("server", 1),
            ("SERVer", 1),
            #
            ("alias", 0),
            ("domain", 0),
            ("domAIn", 0),
            ("bad_username", 0),
            ("ZZZ", 0),
            ("1", 0),
        ]

        for term, count in expected_results:
            results = search_emailuser(term)
            self.assertEqual(len(results), count)

    def test_search_empty(self):
        with self.assertRaises(Exception):
            search_emailaliases(" ")

    def test_search_None(self):
        with self.assertRaises(Exception):
            search_emailaliases(None)

    def test_search_noargs(self):
        with self.assertRaises(Exception):
            search_emailaliases()

    def test_search_by_request_GET(self):
        fake_get_request = namedtuple("request", "GET POST")
        fake_request = fake_get_request({"q": "a", "alias": True, "user": True}, {})
        results = search_from_request(fake_request)

        self.assertEqual(len(results["all_list"]), 2)
        self.assertEqual(len(results["user_list"]), 1)
        self.assertEqual(len(results["alias_list"]), 1)

    def test_search_by_request_POST(self):
        fake_post_request = namedtuple("request", "GET POST")
        fake_request = fake_post_request(
            {},
            {"q": "a", "alias": True, "user": True},
        )
        results = search_from_request(fake_request)

        self.assertEqual(len(results["all_list"]), 2)
        self.assertEqual(len(results["user_list"]), 1)
        self.assertEqual(len(results["alias_list"]), 1)

    def test_search_by_kwarg(self):
        fake_post_request = namedtuple("request", "GET POST")
        fake_request = fake_post_request({}, {})
        results = search_from_request(fake_request, "a")

        self.assertEqual(len(results["all_list"]), 2)
        self.assertEqual(len(results["user_list"]), 1)
        self.assertEqual(len(results["alias_list"]), 1)
