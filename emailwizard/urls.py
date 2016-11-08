from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.contrib.auth.views import login, logout
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    '',
    url(r'^vutman/', include('vutman.urls')),
    url(r'^admin/',  include(admin.site.urls)),
    url(r'^$', RedirectView.as_view(url='/vutman/')),
    url(r'^accounts/login/$',  login),
    url(r'^accounts/logout/$', logout, {'next_page': '/'}),
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
]
