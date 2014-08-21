from django.db import models
from cuser.fields import CurrentUserField
from django.core.urlresolvers import reverse


class VutmanModel(models.Model):
    STATE_CHOICES = (
        ('E', 'Enabled'),
        ('D', 'Disabled'),
        ('X', 'Deleted'),
    )
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default="E")
    last_modified = models.DateField(auto_now=True, auto_now_add=True)
    last_modified_by = CurrentUserField()

    def get_absolute_url(self):
        object_type = self.__class__.__name__.lower()
        return reverse('%s.details' % object_type, args=[str(self.id)])


class EmailServer(VutmanModel):
    email_server = models.CharField(max_length=200)

    def __str__(self):
        return self.email_server


class EmailDomain(VutmanModel):
    domain_name = models.CharField(max_length=200)

    def __str__(self):
        return self.domain_name


class EmailUser(VutmanModel):
    username = models.CharField(max_length=200)
    fullname = models.CharField(max_length=200, blank=True)
    email_server = models.ForeignKey(EmailServer)
    active_directory_basedn = models.CharField(blank=True, max_length=200)

    def __str__(self):
        return self.username

    class Meta:
        unique_together = (("username", "email_server"))


class EmailAlias(VutmanModel):
    alias_name = models.CharField(max_length=50)
    username = models.ForeignKey(EmailUser)
    email_domain = models.ForeignKey(EmailDomain)

    def __str__(self):
        return "%s@%s" % (self.alias_name, self.email_domain)

    class Meta:
        unique_together = (("alias_name", "email_domain"))
        verbose_name_plural = "aliases"
