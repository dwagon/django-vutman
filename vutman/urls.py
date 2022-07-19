from django.urls import path
from vutman import views

urlpatterns = [
    path("search/", views.search, name="search"),
    path("user/<int:pk>", views.emailuser_details, name="emailuser.details"),
    path("user/<int:pk>/delete/", views.emailuser_delete, name="emailuser.delete"),
    path("user/new/", views.emailuser_details, name="emailuser.new"),
    path("alias/<int:pk>/", views.emailalias_details, name="emailalias.details"),
    path("alias/new/", views.emailalias_details, name="emailalias.new"),
    path("alias/<int:pk>/delete/", views.emailalias_delete, name="emailalias.delete"),
    path("render_vut/", views.render_virtual_user_table, name="render_vut"),
    path("", views.index, name="index"),
]
