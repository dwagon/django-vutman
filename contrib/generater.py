#!/usr/local/bin/python2.7
import sys, os
from distutils.sysconfig import get_python_lib
import os.path
sys.path.append(os.path.join(get_python_lib(), "vutman/templates"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'vutman.settings'

from vutman.mail.models import User, Server, Domain, Alias, Raw
import time

def generate_oldalias():
	for raw in Raw.objects.filter(flag__gte=0,flag__lt=10):
		print "%s:\t%s" % ( raw.left, raw.right)

def generate_oldvut():
	for raw in Raw.objects.filter(flag__gte=10):
		print "%s:\t%s" % ( raw.left, raw.right)

def generate_alias():
	print "###############################"
	print "# Alias table"
	print "# For all Domains"
	print "###############################"

	print "###############################"
	print "# aliases"
	print "###############################"
	

def generate_vut():
	vut = open(get_python_lib() + "/vutman/media/virtusertable.txt" ,'w')

	vut.write( "###############################\n" )
	vut.write( "# Virutal User Table:\n" )
	vut.write( "# For all Domains\n" ) 
	vut.write( "# Generated at : " + str(time.time()) + "\n" )
	vut.write( "###############################\n" )

	i = 0

	#for alias in Alias.objects.select_related().filter(user__deleted=0).filter(deleted=0):

	for alias in Alias.objects.select_related().filter(user__deleted=0).filter(deleted=0)[0:100000]:
		try:
		    vut.write( "%s\n" % alias.generate_vut() )
		except UnicodeEncodeError:
			print "UnicodeEncodeError: %s\n" % alias.generate_vut()

	print "flush memory"

	for alias in Alias.objects.select_related().filter(user__deleted=0).filter(deleted=0)[100000:200000]:
		try:
		    vut.write( "%s\n" % alias.generate_vut() )
		except UnicodeEncodeError:
			print "UnicodeEncodeError: %s\n" % alias.generate_vut()

	print "flush memory"

	for alias in Alias.objects.select_related().filter(user__deleted=0).filter(deleted=0)[200000:300000]:
		try:
		    vut.write( "%s\n" % alias.generate_vut() )
		except UnicodeEncodeError:
			print "UnicodeEncodeError: %s\n" % alias.generate_vut()
	print "flush memory"


	#vut.write( "###############################\n" )
	#vut.write( "# Forced postmaster address for websense\n") 
	#vut.write( "###############################\n" )
	#for dmn in Domain.objects.all():
	#	vut.write( "postmaster@%s postmaster@smtpex.toll.com.au\n" % dmn )

	vut.write( "###############################\n" )
	vut.write( "# OLD VUT full domain redirects\n" )
	vut.write( "###############################\n" )
	vut.write( "@faxmaker.com                   %1@smtpex.toll.com.au\n" )
	vut.write( "@frank.toll.com.au              %1@toll.com.au\n" )
	vut.write( "@shipping.brambles.com.au       %1@smtpnt.toll.com.au\n" )
	vut.write( "@creche.toll.com.au             %1@toll.com.au\n" )
	vut.write( "@segv.toll.com.au               %1@toll.com.au\n" )
	vut.write( "@smtpnt.toll.com.au             %1@toll.com.au\n" )


	#vut.write( "###############################\n" )
	#vut.write( "# Drop all emails that are not in this file\n" )
	#vut.write( "###############################\n" )
	#for dmn in Domain.objects.all():
	#	# Drop emails with an error message, for unknown user.
	#	vut.write( "@%s error:nouser User Unknown\n" % dmn )

	vut.write( "###############################\n" )
	vut.write( "#END_OF_FILE\n" )

def generate_smtpex_vut():
	for srv in Server.objects.all().filter(servername="smtpex.toll.com.au"):
		for user in User.objects.filter(servername=srv).order_by('user'):
			for alias in Alias.objects.filter(user=user):
				print alias.generate_vut()

def generate_time():
	
	print "for loop on Alias.objects.all()"
	# Test the lookup and query speed of getting all objects
	start_lookup = time.time()
	c = 0
	for alias in Alias.objects.all():
		left = "%s@%s" %  (alias.alias, alias.domain)
		right = "%s@%s" % (alias.user.mailbox, alias.user.servername)
		c = c + 1
		if c % 1000 == 0:
			print c, time.time() - start_lookup
		if c % 10000 == 0:
			break

	print "Alias.objects.all()"
	# Test the lookup and query speed of getting all objects
	start_lookup = time.time()
	alias_list = Alias.objects.all()
	c = 0
	for alias in alias_list:
		left = "%s@%s" %  (alias.alias, alias.domain)
		right = "%s@%s" % (alias.user.mailbox, alias.user.servername)
		c = c + 1
		if c % 1000 == 0:
			print c, time.time() - start_lookup
		if c % 10000 == 0:
			break

	print "Alias.objects.all().iterator()"
	# Test the lookup and query speed of getting all objects
	start_lookup = time.time()
	alias_list = Alias.objects.all().iterator()
	c = 0
	for alias in alias_list:
		left = "%s@%s" %  (alias.alias, alias.domain)
		right = "%s@%s" % (alias.user.mailbox, alias.user.servername)
		c = c + 1
		if c % 1000 == 0:
			print c, time.time() - start_lookup
		if c % 10000 == 0:
			break

	print "list(Alias.objects.all())"
	# Test the lookup and query speed of getting all objects
	start_lookup = time.time()
	alias_list = list(Alias.objects.all())
	c = 0
	for alias in alias_list:
		left = "%s@%s" %  (alias.alias, alias.domain)
		right = "%s@%s" % (alias.user.mailbox, alias.user.servername)
		c = c + 1
		if c % 1000 == 0:
			print c, time.time() - start_lookup
		if c % 10000 == 0:
			break


	print "Alias.objects.select_related().all()"
	# Test the lookup and query speed of getting all objects
	start_lookup = time.time()
	c = 0
	for alias in Alias.objects.select_related().all():
		left = "%s@%s" %  (alias.alias, alias.domain)
		right = "%s@%s" % (alias.user.mailbox, alias.user.servername)
		c = c + 1
		if c % 1000 == 0:
			print c, time.time() - start_lookup
		if c % 10000 == 0:
			break




	# select CONCAT( a.alias, "@", d.domain, ":") as alias , CONCAT(u.user, "@", s.servername) as user from `opsunix`.`mail_user` as u, `opsunix`.`mail_alias` as a,	`opsunix`.`mail_server` as s,	`opsunix`.`mail_domain` as d WHERE a.user_id = u.id AND u.servername_id = s.id AND a.domain_id = d.id

if sys.argv[1] == "vut":
	generate_vut()

if sys.argv[1] == "alias":
	generate_alias()

if sys.argv[1] == "smptex":
	generate_smtpex_vut()

if sys.argv[1] == "time":
	generate_time()

