""" Test cases for vutman view code """
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from vutman.models import EmailAlias, EmailUser, EmailDomain, EmailServer


class SimpleTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.request_user = User.objects.create_user(
            "admin", "admin@local.host", "password"
        )
        self.request_user.save()
        self.client.login(username="admin", password="password")

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
        self.user2 = EmailUser.objects.create(
            username="username2",
            fullname="first last2",
            email_server=self.server,
            active_directory_basedn="basedn2",
        )
        self.alias2 = EmailAlias.objects.create(
            alias_name="alias2", username=self.user2, email_domain=self.domain
        )

    def test_index_access_login(self):
        self.client.login(username="admin", password="password")
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_search_no_q(self):
        response = self.client.get(reverse("search"), args=[])
        self.assertEqual(response.context, None)
        self.assertEqual(response.status_code, 302)

    def test_search_bad_q(self):
        response = self.client.get(reverse("search"), args={"q": "BAD_SEARCH"})
        self.assertEqual(response.context, None)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("search"), args={"q": ""})
        self.assertEqual(response.context, None)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("search"), args={"q": None})
        self.assertEqual(response.context, None)
        self.assertEqual(response.status_code, 302)

    def test_search_good(self):
        response = self.client.get(
            reverse("search"), {"q": "a", "alias": "on", "user": "on"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context[-1]["all_list"]), 4)
        self.assertEqual(len(response.context[-1]["alias_list"]), 2)
        self.assertEqual(len(response.context[-1]["user_list"]), 2)

    def test_search_good_find_nothing_redirect_index(self):
        response = self.client.get(
            reverse("search"), {"q": "WILL_NOT_MATCH", "alias": "on", "user": "on"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("index"), response.url)

    def test_search_good_find_single_user_redirect_to_page(self):
        response = self.client.get(
            reverse("search"), {"q": "username2", "alias": "on", "user": "on"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.user2.get_absolute_url(), response.url)
        self.assertIn("one_user", response.url)

    def test_search_good_find_single_alias_redirect_to_page(self):
        response = self.client.get(
            reverse("search"), {"q": "alias2", "alias": "on", "user": "on"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.user2.get_absolute_url(), response.url)
        self.assertIn("one_alias", response.url)

    def test_search_only_aliases(self):
        response = self.client.get(reverse("search"), {"q": "a", "alias": "on"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context[-1]["all_list"]), 2)
        self.assertEqual(len(response.context[-1]["alias_list"]), 2)
        self.assertEqual(len(response.context[-1]["user_list"]), 0)

    def test_search_only_users(self):
        response = self.client.get(reverse("search"), {"q": "a", "user": "on"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context[-1]["all_list"]), 2)
        self.assertEqual(len(response.context[-1]["alias_list"]), 0)
        self.assertEqual(len(response.context[-1]["user_list"]), 2)

    def test_search_1users_many_aliases(self):
        # domain = EmailDomain.objects.create(email_server="domain2")
        EmailUser.objects.create(
            username="domain21",
            fullname="first last",
            email_server=self.server,
            active_directory_basedn="basedn",
        ).save()
        EmailUser.objects.create(
            username="domain",
            fullname="first last",
            email_server=self.server,
            active_directory_basedn="basedn",
        ).save()
        EmailAlias.objects.create(
            alias_name="domain2", username=self.user2, email_domain=self.domain
        ).save()
        EmailAlias.objects.create(
            alias_name="domain21", username=self.user, email_domain=self.domain
        ).save()

        response = self.client.get(
            reverse("search"), {"q": "domain2", "user": "on", "alias": "on"}
        )
        self.assertEqual(response.status_code, 200)

    def test_render_vut(self):
        response = self.client.get(reverse("render_vut"))
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(response.context[-1]['alias_list']), 2)

    def test_emailuser_details(self):
        response = self.client.get(self.user.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_emailalias_delete(self):
        response = self.client.get(
            reverse("emailalias.delete", kwargs={"pk": self.alias.pk})
        )
        # messages = self.client.get_and_delete_messages()
        # print(messages)
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.user.get_absolute_url(), response.url)

    def test_emailalias_delete_missing_id(self):
        response = self.client.get(reverse("emailalias.delete", kwargs={"pk": 10000}))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("index"), response.url)

    def test_emaildetails_get(self):
        response = self.client.get(self.user.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.user.get_absolute_url(), {"pk": self.user.pk})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(self.user.get_absolute_url(), {"pk": self.user.pk})
        self.assertEqual(response.status_code, 200)

    def test_aliasdetails_via_bad_post(self):
        response = self.client.post(
            reverse("emailalias.details", kwargs={"pk": self.alias.pk}), {}
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.alias.username.get_absolute_url(), response.url)

    def test_aliasdetails_via_ok_post(self):
        response = self.client.post(
            reverse("emailalias.details", kwargs={"pk": self.alias.pk}),
            {"pk": self.alias.pk, "username": self.user.pk},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.alias.username.get_absolute_url(), response.url)

    def test_aliasdetails_via_good_post(self):
        response = self.client.post(
            reverse("emailalias.details", kwargs={"pk": self.alias.pk}),
            {
                "pk": self.alias.pk,
                "username": self.user.pk,
                "email_domain": self.domain.pk,
                "alias_name": "alias_name",
                "state": "E",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.alias.username.get_absolute_url(), response.url)

    def test_aliasdetails_via_good_post_no_pk(self):
        response = self.client.post(
            reverse("emailalias.new"),
            {
                # 'pk': self.alias.pk,
                "username": self.user.pk,
                "email_domain": self.domain.pk,
                "alias_name": "alias_name",
                "state": "E",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.alias.username.get_absolute_url(), response.url)

    def test_aliasdetails_via_good_post_via_userdetails(self):
        response = self.client.post(
            reverse("emailuser.details", kwargs={"pk": self.user.pk}),
            {
                "pk": self.alias.pk,
                "username": self.user.pk,
                "email_domain": self.domain.pk,
                "alias_name": "new_alias_name_via_post",
                "state": "E",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_userdetails_via_post(self):
        response = self.client.post(
            reverse("emailuser.details", kwargs={"pk": self.user.pk}), {}
        )
        self.assertEqual(response.status_code, 200)

    def test_userdetails_via_post_bad_pk(self):
        response = self.client.post(
            reverse("emailuser.details", kwargs={"pk": 10000}), {}
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("index"), response.url)

    def test_userdetails_via_post_good_pk(self):
        response = self.client.post(
            reverse("emailuser.details", kwargs={"pk": self.user.pk}),
        )
        self.assertEqual(response.status_code, 200)

    def test_userdetails_via_post_good_form(self):
        response = self.client.post(
            reverse("emailuser.details", kwargs={"pk": self.user.pk}),
            {
                "pk": self.user.pk,
                "username": "new_username_set_by_post",
                "email_server": self.server.pk,
                "full_name": "new_fullname_set_by_post",
                "state": "E",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.user.get_absolute_url(), response.url)

    def test_userdetails_via_post_bad_alias(self):
        response = self.client.post(
            reverse("emailuser.details", kwargs={"pk": self.user.pk}),
            {
                "alias_name": "",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_userdetails_via_post_good_form_to_user_user(self):
        response = self.client.post(
            reverse("emailuser.new"),
            {
                "username": "new_username_set_by_post",
                "email_server": self.server.pk,
                "full_name": "new_fullname_set_by_post",
                "state": "E",
            },
            follow=True,
        )
        # self.assertIn(EmailUser(pk=3).get_absolute_url(), response.path)
        self.assertEqual(response.status_code, 200)

    def test_userdetails_has_new_form(self):
        response = self.client.get(reverse("emailuser.new"))
        self.assertEqual(response.status_code, 200)

    def test_emailuser_delete(self):
        response = self.client.get(
            reverse("emailuser.delete", kwargs={"pk": self.user.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("index"), response.url)

    def test_emailuser_delete_missing_id(self):
        response = self.client.get(reverse("emailuser.delete", kwargs={"pk": 10000}))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("index"), response.url)
