from django.contrib import admin
from vutman.models import EmailDomain, EmailServer, EmailUser, EmailAlias
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(EmailDomain, SimpleHistoryAdmin)
admin.site.register(EmailServer, SimpleHistoryAdmin)
admin.site.register(EmailUser, SimpleHistoryAdmin)
admin.site.register(EmailAlias, SimpleHistoryAdmin)
