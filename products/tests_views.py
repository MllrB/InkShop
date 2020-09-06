"""
Automated testing for products.models
"""
from django.test import TestCase
from decimal import Decimal
from .models import Category, ProductGroup, VatGroup, Supplies


class TestProductsViews(TestCase):

    def test_get_all_products(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
