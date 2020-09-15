"""
Products app urls
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('product_detail/<product_id>/',
         views.product_detail, name='product_detail'),
    path('add_to_favourites/<product_id>/',
         views.add_to_favourites, name='add_to_favourites'),
    path('remove_from_favourites/<product_id>/',
         views.remove_from_favourites, name='remove_from_favourites'),
]
