"""
Customer app urls
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('<template_target>/', views.show_profile, name='user_profile'),
    path('add_delivery_address/<template_target>/', views.add_delivery_address,
         name='add_delivery_address'),
]
