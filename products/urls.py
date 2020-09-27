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
    path('product_maintenance/',
         views.product_maintenance, name='product_maintenance'),
    path('product_maintenance/update_prices/',
         views.update_prices, name='update_prices'),
    path('product_maintenance/add_p_group/',
         views.add_product_group, name='add_p_group'),
    path('product_maintenance/update_p_group/<group_id>/',
         views.update_product_group, name='update_p_group'),
    path('product_maintenance/add_v_group/',
         views.add_vat_group, name='add_v_group'),
    path('product_maintenance/update_v_group/<group_id>/',
         views.update_vat_group, name='update_v_group'),
    path('product_maintenance/update_category/<category_id>/',
         views.update_category, name='update_category'),
    path('product_maintenance/edit_products/',
         views.edit_products, name='edit_products'),
]
