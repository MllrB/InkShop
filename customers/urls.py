"""
Customer app urls
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_profile, name='user_profile'),
]
