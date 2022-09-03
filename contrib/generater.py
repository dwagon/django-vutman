#!/usr/bin/env python3
""" Generate a virtual user table from Vutman """
# pylint: disable=no-member, wrong-import-position
import argparse
import os
import os.path
import sys
import time
from distutils.sysconfig import get_python_lib

sys.path.append(os.path.join(get_python_lib(), "vutman/templates"))
os.environ["DJANGO_SETTINGS_MODULE"] = "emailwizard.settings"
import django

django.setup()
from vutman.models import EmailUser, EmailServer, EmailAlias


##############################################################################
def generate_alias():
    """TODO"""
    print("###############################")
    print("# Alias table")
    print("# For all Domains")
    print("###############################")

    print("###############################")
    print("# aliases")
    print("###############################")


##############################################################################
def generate_vut(fname=None):
    """TODO"""
    if fname is None:
        fname = os.path.join(get_python_lib(), "vutman/media/virtusertable.txt")
    with open(fname, "w", encoding="utf-8") as vut:
        vut.write("###############################\n")
        vut.write("# Virutal User Table:\n")
        vut.write("# For all Domains\n")
        vut.write(f"# Generated at: {time.ctime()}\n")
        vut.write("###############################\n")

        for alias in (
            EmailAlias.objects.select_related().filter(username__state="E").filter(state="E")
        ):
            vut.write(f"{alias.vut_entry()}\n")

        vut.write("###############################\n")
        vut.write("# OLD VUT full domain redirects\n")
        vut.write("###############################\n")
        vut.write("@faxmaker.com                   %1@smtpex.toll.com.au\n")
        vut.write("@frank.toll.com.au              %1@toll.com.au\n")
        vut.write("@shipping.brambles.com.au       %1@smtpnt.toll.com.au\n")
        vut.write("@creche.toll.com.au             %1@toll.com.au\n")
        vut.write("@segv.toll.com.au               %1@toll.com.au\n")
        vut.write("@smtpnt.toll.com.au             %1@toll.com.au\n")
        vut.write("###############################\n")
        vut.write("#END_OF_FILE\n")


##############################################################################
def generate_smtpex_vut():
    """TODO"""
    for srv in EmailServer.objects.all().filter(email_server="smtpex.toll.com.au"):
        for user in EmailUser.objects.filter(email_server=srv).order_by("username"):
            for alias in EmailAlias.objects.filter(username=user):
                print(alias.vut_entry())


##############################################################################
def parse_args():
    """ Parse command line arguments """
    parser = argparse.ArgumentParser(description='Generate virtual user table from VUTMAN')
    parser.add_argument('--output', help="Destination file")
    parser.add_argument("command", help="What to generate")
    args = parser.parse_args()
    return args


##############################################################################
def main():
    """ Main """
    args = parse_args()
    if args.command == "vut":
        generate_vut(args.output)

    if args.command == "alias":
        generate_alias()

    if args.command == "smptex":
        generate_smtpex_vut()


##############################################################################
if __name__ == "__main__":
    main()
