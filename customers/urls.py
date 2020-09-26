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
    path('update_delivery_address/<address_id>/', views.update_delivery_address,
         name='update_delivery_address'),
    path('delete_delivery_address/<address_id>/', views.delete_delivery_address,
         name='delete_delivery_address'),
    path('delete_favourited_product/<product_id>/', views.delete_favourited_product,
         name='delete_favourited_product'),
    path('repeat_order/<order_id>/', views.repeat_order, name='repeat_order'),
]
