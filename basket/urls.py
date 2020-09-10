"""
Basket app urls
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_basket, name='show_basket'),
]
