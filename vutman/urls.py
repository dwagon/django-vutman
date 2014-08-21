from django.conf.urls import url, include
from vutman import views

urlpatterns = [
    url(r'^search/$', views.search, name='search'),

    url(r'^user/(\d+)/$', views.emailuser_details, name='emailuser.details'),
    url(r'^alias/(\d+)/$', views.emailalias_details, name='emailalias.details'),

    url(r'^$', views.index, name='index'),
]
