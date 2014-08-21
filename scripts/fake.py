from vutman.models import EmailUser, EmailServer, EmailAlias, EmailDomain
import random


def run():
    FAKE_SERVERS = 5
    FAKE_USERS = 20
    emailserver_list = []
    emaildomain_list = []
    for i in range(FAKE_SERVERS):
        o = EmailServer.objects.create(email_server="server_%d" % i)
        o.save()
        emailserver_list.append(o)

        o = EmailDomain.objects.create(domain_name="domain_%d" % i)
        o.save()
        emaildomain_list.append(o)

    for i in range(FAKE_USERS):
        print i
        o = EmailUser.objects.create(
            username="username_%d" % i,
            fullname="fullname_%d" % i,
            email_server=random.choice(emailserver_list)
        )
        o.save()
        e = EmailAlias.objects.create(
            alias_name="alias_%d" % i,
            username=o,
            email_domain=random.choice(emaildomain_list)
        )
        e.save()
