from django.conf.urls import url
from vutman import views

urlpatterns = [
    url(r'^search/$', views.search, name='search'),

    url(r'^user/(\d+)/$', views.emailuser_details, name='emailuser.details'),
    url(r'^alias/(\d+)/$', views.emailalias_details,
        name='emailalias.details'),
    url(r'^alias/new/$', views.emailalias_details,
        name='emailalias.details'),
    url(r'^alias/(\d+)/delete/$', views.emailalias_delete,
        name='emailalias.delete'),

    url(r'^render_vut/$', views.render_virtual_user_table),

    url(r'^$', views.index, name='index'),
]
