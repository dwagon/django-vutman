#!/bin/bash
rm db.sqlite3
./manage.py syncdb --noinput
./manage.py createsuperuser --noinput --email="admin@localhost.com" --username="admin"
./manage.py set_fake_passwords --password="admin"
./manage.py runscript fake

./manage.py runserver
