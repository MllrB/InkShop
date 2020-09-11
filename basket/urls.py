"""
Basket app urls
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_basket, name='show_basket'),
    path('add/<product_id>/', views.add_to_basket, name='add_to_basket'),
]
