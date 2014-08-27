from django.test import TestCase, Client
from vutman.models import EmailAlias, EmailUser, EmailDomain, EmailServer
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class SimpleTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.request_user = User.objects.create_user('admin',
                                                     'admin@local.host',
                                                     'password'
                                                     )
        self.request_user.save()
        self.client.login(username="admin",
                          password="password")

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
        self.user2 = EmailUser.objects.create(
            username="username2",
            fullname="first last2",
            email_server=self.server,
            active_directory_basedn="basedn2"
        )
        self.alias2 = EmailAlias.objects.create(
            alias_name="alias2",
            username=self.user2,
            email_domain=self.domain
        )

    def test_index_access_login(self):
        self.client.login(username="admin",
                          password="password")
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_search_no_q(self):
        return
        response = self.client.get(reverse('search'), args=[])
        self.assertEqual(response.context, None)
        self.assertEqual(response.status_code, 302)

    def test_search_bad_q(self):
        return
        response = self.client.get(reverse('search'), args={'q': 'BAD_SEARCH'})
        self.assertEqual(response.context, None)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('search'), args={'q': ''})
        self.assertEqual(response.context, None)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('search'), args={'q': None})
        self.assertEqual(response.context, None)
        self.assertEqual(response.status_code, 302)

    def test_search_good(self):
        response = self.client.get(reverse('search'),
                                   {'q': 'a', 'alias': 'on', 'user': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context[-1]['all_list']), 4)
        self.assertEqual(len(response.context[-1]['alias_list']), 2)
        self.assertEqual(len(response.context[-1]['user_list']), 2)

    def test_search_only_aliases(self):
        response = self.client.get(reverse('search'),
                                   {'q': 'a', 'alias': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context[-1]['all_list']), 2)
        self.assertEqual(len(response.context[-1]['alias_list']), 2)
        self.assertEqual(len(response.context[-1]['user_list']), 0)

    def test_search_only_users(self):
        response = self.client.get(reverse('search'),
                                   {'q': 'a', 'user': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context[-1]['all_list']), 2)
        self.assertEqual(len(response.context[-1]['alias_list']), 0)
        self.assertEqual(len(response.context[-1]['user_list']), 2)

    def test_render_vut(self):
        response = self.client.get(reverse('render_vut'))
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(response.context[-1]['alias_list']), 2)

    def test_emailuser_details(self):
        response = self.client.get(self.user.get_absolute_url())
        self.assertEqual(response.status_code, 200)
