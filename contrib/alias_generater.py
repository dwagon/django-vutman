#!/usr/bin/env python
import sys, os
from distutils.sysconfig import get_python_lib
import os.path
sys.path.append(os.path.join(get_python_lib(), "vutman/templates"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'vutman.settings'

from vutman.mail.models import User, Server, Domain, Alias, Raw
from django.db.models import Q
import time

def generate_oldalias():
	for raw in Raw.objects.filter(flag__gte=0,flag__lt=10):
		print "%s:\t%s" % ( raw.left, raw.right)

def generate_oldvut():
	for raw in Raw.objects.filter(flag__gte=10):
		print "%s:\t%s" % ( raw.left, raw.right)

def generate_alias():
	print "##########################################################################"
	print "# aliases replace file generated from vutman"
	print "# every address will look like the below"
	print "# alias:	user@server"
	print "##########################################################################"
	
	last_alias = ""

	tollgroup_com = Domain.objects.get(domain="tollgroup.com")
	toll_com_au = Domain.objects.get(domain="toll.com.au")

	count = Alias.objects.filter(Q(domain=tollgroup_com ) | Q(domain=toll_com_au)).order_by('alias','user').count()
	#for alias in Alias.objects.filter(Q(domain=tollgroup_com ) | Q(domain=toll_com_au)).filter(user__deleted=0).order_by('alias','user').filter(deleted=0):

	for alias in Alias.objects.filter(Q(domain=tollgroup_com ) | Q(domain=toll_com_au)).order_by('alias','user')[0:100000]:
		if last_alias == alias.alias:
			continue
		try:
			print "%s:\t\t%s@%s" % ( alias.alias, alias.user.mailbox.replace(' ',''), alias.user.servername )
		except UnicodeEncodeError:
			pass
		last_alias = alias.alias

	for alias in Alias.objects.filter(Q(domain=tollgroup_com ) | Q(domain=toll_com_au)).order_by('alias','user')[100000:200000]:
		if last_alias == alias.alias:
			continue
		try:
			print "%s:\t\t%s@%s" % ( alias.alias, alias.user.mailbox.replace(' ',''), alias.user.servername )
		except UnicodeEncodeError:
			pass
		last_alias = alias.alias


	for alias in Alias.objects.filter(Q(domain=tollgroup_com ) | Q(domain=toll_com_au)).order_by('alias','user')[200000:]:
		if last_alias == alias.alias:
			continue
		try:
			print "%s:\t\t%s@%s" % ( alias.alias, alias.user.mailbox.replace(' ',''), alias.user.servername )
		except UnicodeEncodeError:
			pass
		last_alias = alias.alias


	print "#########################################################################"
	print "#END_OF_FILE"

def generate_vut():
	vut = open(get_python_lib() + "/vutman/media/virtusertable.txt" ,'w')

	vut.write( "###############################\n" )
	vut.write( "# Virutal User Table:\n" )
	vut.write( "# For all Domains\n" ) 
	vut.write( "# Generated at : " + str(time.time()) + "\n" )
	vut.write( "###############################\n" )

	for alias in Alias.objects.select_related().all():
		vut.write( alias.generate_vut() + "\n" )

	vut.write( "###############################\n" )
	vut.write( "# Forced postmaster address for websense\n") 
	vut.write( "###############################\n" )
	for dmn in Domain.objects.all():
		vut.write( "postmaster@%s postmaster@smtpex.toll.com.au\n" % dmn )

	vut.write( "###############################\n" )
	vut.write( "# OLD VUT full domain redirects\n" )
	vut.write( "###############################\n" )
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
	vut.write( "# END OF FILE\n" )
	vut.write( "###############################\n" )

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

