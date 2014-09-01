from django.test import TestCase
from vutman.models import EmailAlias, EmailUser, EmailDomain, EmailServer
from vutman.scripts import generate_vut_to_file


class SimpleTestCase(TestCase):
    def setUp(self):
        self.server = EmailServer.objects.create(email_server="server")
        self.domain = EmailDomain.objects.create(domain_name="domain")
        self.user = EmailUser.objects.create(
            username="username",
            fullname="first last",
            email_server=self.server,
            active_directory_basedn="basedn"
        )
        self.alias = EmailAlias.objects.create(
            alias_name="alias",
            username=self.user,
            email_domain=self.domain
        )

    def test_generate_vut_to_file(self):
        test_file = "/tmp/test_generated_file"
        generate_vut_to_file(test_file)
        self.assertEqual(open(test_file).read(),
                         "alias@domain: username@server\n")

    def test_generate_vut_to_file_no_aliases(self):
        test_file = "/tmp/test_generated_file"
        self.alias.delete()
        generate_vut_to_file(test_file)
        self.assertEqual(open(test_file).read(), "")

    def test_generate_vut_to_file_no_users(self):
        test_file = "/tmp/test_generated_file"
        self.user.delete()
        generate_vut_to_file(test_file)
        self.assertEqual(open(test_file).read(), "")

    def test_generate_vut_to_file_many_aliases(self):
        for i in range(0, 5):
            EmailAlias.objects.create(
                alias_name="alias_%s" % i,
                username=self.user,
                email_domain=self.domain
            )
            test_file = "/tmp/test_generated_file"
            generate_vut_to_file(test_file)
            self.assertIn("alias_%s@domain: username@server\n" % i,
                          open(test_file).readlines())
