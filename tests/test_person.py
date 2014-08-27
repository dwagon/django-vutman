from django.test import TestCase
from vutman.models import EmailAlias, EmailUser, EmailDomain, EmailServer
from django.db import IntegrityError


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

    def test_duplicate_users(self):
        server1 = EmailServer.objects.create(email_server="server1")
        server2 = EmailServer.objects.create(email_server="server2")

        EmailUser.objects.create(
            username="user1",
            email_server=server1
        )
        EmailUser.objects.create(
            username="user2",
            email_server=server1
        )
        EmailUser.objects.create(
            username="user1",
            email_server=server2
        )
        with self.assertRaises(IntegrityError):
            EmailUser.objects.create(
                username="user1",
                email_server=server1
            )

    def test_duplicate_alias(self):
        domain1 = EmailDomain.objects.create(domain_name="domain1")
        domain2 = EmailDomain.objects.create(domain_name="domain2")

        EmailAlias.objects.create(
            alias_name="alias1",
            username=self.user,
            email_domain=domain1
        )
        EmailAlias.objects.create(
            alias_name="alias2",
            username=self.user,
            email_domain=domain1
        )
        EmailAlias.objects.create(
            alias_name="alias1",
            username=self.user,
            email_domain=domain2
        )

        with self.assertRaises(IntegrityError):
            EmailAlias.objects.create(
                alias_name="alias1",
                username=self.user,
                email_domain=domain1
            )

    def test_disable(self):
        self.assertEqual(self.user.state, 'E')
        last_modified = self.user.last_modified
        self.user.disable()
        last_modified2 = self.user.last_modified
        self.assertEqual(self.user.state, 'D')
        self.assertNotEqual(last_modified, last_modified2)

    def test_user(self):
        self.assertEqual(self.user.username, 'username')
        self.assertEqual(self.user.fullname, 'first last')
        self.assertEqual(self.user.email_server, self.server)

    def test_user_default_state(self):
        self.assertEqual(self.user.state, 'E')

    def test_autoupdate_lastmodified(self):
        last_modified = self.user.last_modified
        last_modified2 = self.user.last_modified
        self.assertEqual(last_modified, last_modified2)
        self.user.fullname = "recently updated"
        self.user.save()
        last_modified3 = self.user.last_modified
        self.assertNotEqual(last_modified, last_modified3)

    def test_absolute_urls(self):
        self.assertEqual(self.user.get_absolute_url(),
                         '/vutman/user/%d/' % self.user.pk)
        self.assertEqual(self.alias.get_absolute_url(),
                         '/vutman/alias/%d/' % self.alias.pk)

        with self.assertRaises(Exception):
            self.server.get_absolute_url()
        with self.assertRaises(Exception):
            self.domain.get_absolute_url()

    def test_suggested_aliases(self):
        aliases = self.user._suggested_aliases()
        self.assertIn('first.last', aliases)
        self.assertIn('flast', aliases)
        self.assertIn('username', aliases)
        self.assertEqual(len(aliases), 3)

    def test_suggested_aliases_no_dup(self):

        aliases1 = self.user.suggested_aliases()
        self.assertIn('username', aliases1)
        EmailAlias.objects.create(
            alias_name="username",
            username=self.user,
            email_domain=self.domain
        ).save()
        aliases2 = self.user.suggested_aliases()
        aliases_raw = self.user._suggested_aliases()
        self.assertNotIn('username', aliases2)
        self.assertIn('username', aliases_raw)

    def test_generated_vut(self):
        vut = self.alias.vut_entry()
        self.assertEqual(vut, "alias@domain: username@server")

    def test_user_guessname(self):
        EmailAlias.objects.create(
            alias_name="first.last",
            username=self.user,
            email_domain=self.domain
        )
        self.assertEqual(self.user.guess_fullname(), "first last")
        EmailAlias.objects.create(
            alias_name="first_last",
            username=self.user,
            email_domain=self.domain
        )
        self.assertEqual(self.user.guess_fullname(), "first last")

    def test_alias_set_guessname_blank(self):
        self.user.fullname = ''
        self.user.save()

        EmailAlias.objects.create(
            alias_name="new.name",
            username=self.user,
            email_domain=self.domain
        )
        self.user.set_guessed_name()
        self.assertEqual(self.user.fullname, "new name")

    def test_alias_set_guessname(self):
        EmailAlias.objects.create(
            alias_name="new.name",
            username=self.user,
            email_domain=self.domain
        )
        self.user.set_guessed_name()
        self.assertNotEqual(self.user.fullname, "new name")
        self.assertEqual(self.user.fullname, "first last")

    def test_history_object(self):
        history = self.user.history.all()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].username, self.user.username)
        self.assertEqual(history[0].fullname, self.user.fullname)
        self.user.fullname = "new fullname"
        self.user.save()
        self.user.fullname = "newest fullname"
        self.user.save()

        history = self.user.history.all()
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0].fullname, "newest fullname")
        self.assertEqual(history[1].fullname, "new fullname")
        self.assertEqual(history[2].fullname, "first last")

    def test_better_user_history_list(self):
        history = self.user.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0].changed.keys(), [])

        self.user.fullname = "new fullname"
        self.user.save()

        history = self.user.get_history()
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0].changed.keys(), [])
        self.assertEqual(history[1].changed.keys(), ['fullname'])
        self.assertEqual(history[1].changed['fullname'], ('first last', 'new fullname'))

        self.user.fullname = "newest fullname"
        self.user.active_directory_basedn = "new basedn"
        self.user.save()

        history = self.user.get_history()
        self.assertEqual(len(history), 4)
        self.assertEqual(history[0].changed.keys(), [])
        self.assertIn('fullname', history[1].changed.keys())
        self.assertIn('active_directory_basedn', history[1].changed.keys())
        self.assertEqual(history[2].changed.keys(), ['fullname'])

    def test_better_alias_history_list(self):
        history = self.alias.get_history()
        self.assertEqual(len(history), 1)

        self.alias.alias_name = "new fullname"
        self.alias.save()

        history = self.alias.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0].changed.keys(), ['alias_name'])

    def test_usera_alias_history(self):
        history = self.user.get_alias_history()
        self.assertEqual(len(history), 1)
        self.alias.alias_name = "new alias"
        self.alias.save()
        history = self.user.get_alias_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0].changed.keys(), ['alias_name'])

        x = EmailAlias.objects.create(
            alias_name="new.name",
            username=self.user,
            email_domain=self.domain
        )
        x.save()
        x.alias_name = "bob"
        x.save()

        history = self.user.get_alias_history()
        self.assertEqual(len(history), 4)
