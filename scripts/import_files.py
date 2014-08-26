from vutman.models import EmailUser, EmailServer, EmailAlias, EmailDomain
import os
import sys


def run(filename):
    print "Skipping imported names, etc"

    #
    email_server_list = EmailServer.objects.all()
    email_server_name_list = [str(es.email_server) for es in email_server_list]
    #
    email_domain_list = EmailDomain.objects.all()
    email_domain_name_list = [str(dn.domain_name) for dn in email_domain_list]
    #
    email_user_list = EmailUser.objects.all()
    email_user_name_list = [str(eu.username) for eu in email_user_list]

    if filename and not os.path.exists(filename):
        print("can't find file: %s" % filename)
        sys.exit(1)

    for line in open(filename).readlines():
        # skip comments
        if line.startswith("#"):
            continue
        line = line.strip()
        (alias_and_domain, user_and_server) = line.split(':')
        if '@' in alias_and_domain:
            (alias, domain) = alias_and_domain.strip().split('@')
        else:
            alias = alias_and_domain.strip()
            domain = None

        if '@' not in user_and_server:
            continue

        (user, server) = user_and_server.strip().split('@')

        if domain not in email_domain_name_list:
            dn = EmailDomain.objects.create(domain_name=domain)
            dn.save()
            email_domain_name_list.append(domain)
        else:
            dn = EmailDomain.objects.get(domain_name=domain)

        if server not in email_server_name_list:
            es = EmailServer.objects.create(email_server=server)
            es.save()
            email_server_name_list.append(server)
        else:
            es = EmailServer.objects.get(email_server=server)

        if user not in email_user_name_list:
            print user
            eu = EmailUser.objects.create(
                username=user,
                email_server=es
            )
            eu.save()
            email_user_name_list.append(user)
        else:
            eu = EmailUser.objects.filter(username=user)[0]

        try:
            ea = EmailAlias.objects.create(
                alias_name=alias,
                email_domain=dn,
                username=eu
            )
            ea.save()
            eu.set_guessed_name()
        except Exception:
            pass
