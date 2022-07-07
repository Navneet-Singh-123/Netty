from django.contrib import admin
from django.urls import path
from netty import views

urlpatterns = [
    path('device/<slug:slug>', views.get_device_from_slug),
    path('users/auth', views.authenticate),
    path('users', views.all_users), 
    path('users/<slug:slug>', views.user),
]
