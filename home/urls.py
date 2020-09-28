"""
Home app urls
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('account/', views.login, name='account'),
    path('category/<category>', views.get_categories, name='categories'),
    path('about/', views.show_about_us, name='about'),
    path('delivery_info/', views.show_delivery_info, name='delivery_info'),
    path('faqs/', views.show_faqs, name='faqs'),
    path('terms_and_conditions/', views.show_terms, name='terms'),
    path('privacy_policy/', views.show_privacy_policy, name='privacy'),
    path('privacy_policy/', views.show_privacy_policy, name='privacy'),
    path('content_management/', views.content_management,
         name='content_management'),
    path('content_management/save_changes/', views.save_content_changes,
         name='save_content_changes'),
]
