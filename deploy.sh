#!/bin/bash -x

ssh dansysadm.com mkdir -p /var/tmp/djago-emails/
git archive --format=tar.gz HEAD > x.tar
scp -rp x.tar dansysadm.com:/var/tmp/django-emails/
ssh dansysadm.com "(cd /var/tmp/django-emails/; tar xf x.tar)"
# ssh dansysadm.com "(cd /var/tmp/django-emails/; workon vutman; pip install -r requirements.txt)"
ssh dansysadm.com "(cd /var/tmp/django-emails/; source /usr/local/bin/virtualenvwrapper.sh; workon vutman; bash -x ./resetdb.sh)"


