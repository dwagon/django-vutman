[![Coverage Status](https://coveralls.io/repos/daniellawrence/django-vutman/badge.png?branch=master)](https://coveralls.io/r/daniellawrence/django-vutman?branch=master)
[![Build Status](https://travis-ci.org/daniellawrence/django-vutman.svg?branch=master)](https://travis-ci.org/daniellawrence/django-vutman)

Django-vutman
================

Manage your virtual user table via the web!.


How to install
-----------------


    apt-get install python-pip python-dev git
	yum install python-pip python-devel git
	sudo pip install -U pip virtualenv virutalenvwrapper
	source /usr/local/bin/virtualenvwrapper.sh

	git clone https://github.com/daniellawrence/django-vutman
	cd django-vutman
	mkvirtualenv djangovutman
	workon djangovutman
	pip intall -U -r requirements.txt

Running
-------

Running with some fake data...

	./resetdb.sh

Running without trashing the database

	./manage.py runserver [0.0.0.0:8000]

