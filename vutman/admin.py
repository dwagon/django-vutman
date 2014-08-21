from django.contrib import admin
from vutman.models import EmailDomain, EmailServer, EmailUser, EmailAlias

admin.site.register(EmailDomain)
admin.site.register(EmailServer)
admin.site.register(EmailUser)
admin.site.register(EmailAlias)
