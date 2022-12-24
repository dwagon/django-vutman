#!/opt/vutman/bin/python3
import sys, os
from distutils.sysconfig import get_python_lib
import os.path

sys.path.append("/opt/vutman/django-vutman")
os.environ["DJANGO_SETTINGS_MODULE"] = "emailwizard.settings"

import django
django.setup()

from vutman.models import EmailUser, EmailServer, EmailDomain, EmailAlias
from django.db.models import Q
import time


def generate_alias():
    print("##########################################################################")
    print("# aliases replace file generated from vutman")
    print("# every address will look like the below")
    print("# alias:	user@server")
    print("##########################################################################")

    last_alias = ""

    tollgroup_com = EmailDomain.objects.get(domain_name="tollgroup.com")
    toll_com_au = EmailDomain.objects.get(domain_name="toll.com.au")

    count = (
        EmailAlias.objects.filter(Q(email_domain=tollgroup_com) | Q(email_domain=toll_com_au))
        .order_by("alias_name", "username")
        .count()
    )
    # for alias in EmailAlias.objects.filter(Q(email_domain=tollgroup_com ) | Q(email_domain=toll_com_au)).filter(user__deleted=0).order_by('alias','user').filter(deleted=0):

    for alias in EmailAlias.objects.filter(Q(email_domain=tollgroup_com) | Q(email_domain=toll_com_au)).order_by(
        "alias_name", "username"
    )[0:100000]:
        if last_alias == alias.alias_name:
            continue
        try:
            print(f"{alias.alias_name}:\t\t{alias.username}@{alias.username.email_server}")
        except UnicodeEncodeError:
            pass
        last_alias = alias.alias_name

    for alias in EmailAlias.objects.filter(Q(email_domain=tollgroup_com) | Q(email_domain=toll_com_au)).order_by(
        "alias_name", "username"
    )[100000:200000]:
        if last_alias == alias.alias_name:
            continue
        try:
            print(f"{alias.alias_name}:\t\t{alias.username}@{alias.username.email_server}")
        except UnicodeEncodeError:
            pass
        last_alias = alias.alias_name

    for alias in EmailAlias.objects.filter(Q(email_domain=tollgroup_com) | Q(email_domain=toll_com_au)).order_by(
        "alias_name", "username"
    )[200000:]:
        if last_alias == alias.alias_name:
            continue
        try:
            print(f"{alias.alias_name}:\t\t{alias.username}@{alias.username.email_server}")
        except UnicodeEncodeError:
            pass
        last_alias = alias.alias_name

    print("#########################################################################")
    print("#END_OF_FILE")


def generate_vut():
    with open("/opt/vutman/media/virtusertable.txt", "w") as vut:
        vut.write("###############################\n")
        vut.write("# Virutal User Table:\n")
        vut.write("# For all Domains\n")
        vut.write("# Generated at : " + str(time.time()) + "\n")
        vut.write("###############################\n")

        for alias in EmailAlias.objects.select_related().all():
            vut.write(alias.vut_entry() + "\n")

        vut.write("###############################\n")
        vut.write("# Forced postmaster address for websense\n")
        vut.write("###############################\n")
        for dmn in EmailDomain.objects.all():
            vut.write("postmaster@%s postmaster@smtpex.toll.com.au\n" % dmn)

        vut.write("###############################\n")
        vut.write("# OLD VUT full domain redirects\n")
        vut.write("###############################\n")
        vut.write("@frank.toll.com.au              %1@toll.com.au\n")
        vut.write("@shipping.brambles.com.au       %1@smtpnt.toll.com.au\n")
        vut.write("@creche.toll.com.au             %1@toll.com.au\n")
        vut.write("@segv.toll.com.au               %1@toll.com.au\n")
        vut.write("@smtpnt.toll.com.au             %1@toll.com.au\n")

        # vut.write( "###############################\n" )
        # vut.write( "# Drop all emails that are not in this file\n" )
        # vut.write( "###############################\n" )
        # for dmn in EmailDomain.objects.all():
        # 	# Drop emails with an error message, for unknown user.
        # 	vut.write( "@%s error:nouser User Unknown\n" % dmn )

        vut.write("###############################\n")
        vut.write("# END OF FILE\n")
        vut.write("###############################\n")


def generate_smtpex_vut():
    for srv in EmailServer.objects.all().filter(email_server="smtpex.toll.com.au"):
        for user in EmailUser.objects.filter(email_server=srv).order_by("username"):
            for alias in EmailAlias.objects.filter(username=user):
                print(alias.vut_entry())


def generate_time():
    print("for loop on EmailAlias.objects.all()")
    # Test the lookup and query speed of getting all objects
    start_lookup = time.time()
    c = 0
    for alias in EmailAlias.objects.all():
        left = f"{alias.alias_name}@{alias.email_domain}"
        right = f"{alias.username.username}@{alias.username.email_server}"
        c += 1
        if c % 1000 == 0:
            print(c, time.time() - start_lookup)
        if c % 10000 == 0:
            break

    print("EmailAlias.objects.all()")
    # Test the lookup and query speed of getting all objects
    start_lookup = time.time()
    alias_list = EmailAlias.objects.all()
    c = 0
    for alias in alias_list:
        left = f"{alias.alias_name}@{alias.email_domain}"
        right = f"{alias.username.username}@{alias.username.email_server}"
        c += 1
        if c % 1000 == 0:
            print(c, time.time() - start_lookup)
        if c % 10000 == 0:
            break

    print("EmailAlias.objects.all().iterator()")
    # Test the lookup and query speed of getting all objects
    start_lookup = time.time()
    alias_list = EmailAlias.objects.all().iterator()
    c = 0
    for alias in alias_list:
        left = f"{alias.alias_name}@{alias.email_domain}"
        right = f"{alias.username.username}@{alias.username.email_server}"
        c += 1
        if c % 1000 == 0:
            print(c, time.time() - start_lookup)
        if c % 10000 == 0:
            break

    print("list(EmailAlias.objects.all())")
    # Test the lookup and query speed of getting all objects
    start_lookup = time.time()
    alias_list = list(EmailAlias.objects.all())
    c = 0
    for alias in alias_list:
        left = f"{alias.alias_name}@{alias.email_domain}"
        right = f"{alias.username.username}@{alias.username.email_server}"
        c += 1
        if c % 1000 == 0:
            print(c, time.time() - start_lookup)
        if c % 10000 == 0:
            break

    print("EmailAlias.objects.select_related().all()")
    # Test the lookup and query speed of getting all objects
    start_lookup = time.time()
    c = 0
    for alias in EmailAlias.objects.select_related().all():
        left = f"{alias.alias_name}@{alias.email_domain}"
        right = f"{alias.username.username}@{alias.username.email_server}"
        c += 1
        if c % 1000 == 0:
            print(c, time.time() - start_lookup)
        if c % 10000 == 0:
            break

##############################################################################
if sys.argv[1] == "vut":
    generate_vut()

if sys.argv[1] == "alias":
    generate_alias()

if sys.argv[1] == "smptex":
    generate_smtpex_vut()

if sys.argv[1] == "time":
    generate_time()

# EOF
