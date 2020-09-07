"""
Automated testing for products.models
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.db.models import Q
from .models import Category, ProductGroup, VatGroup, Supplies
from .views import all_products


class TestProductsViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.all_products_url = reverse('products')
        self.home_url = reverse('home')
        self.category = Category.objects.create(name='Test_Category')
        self.product_group = ProductGroup.objects.create(
            name='Test_Product_Group')
        self.vat_group = VatGroup.objects.create(name='Test_Vat_Group')
        self.product = Supplies.objects.create(
            skus=["N9K08AE", "N9K08A"],
            name="304XL",
            title="HP 304XL Original Black",
            description="304XL Black Original Ink Cartridge",
            blurb="Print the v",
            related_printers=[
                {
                    "printer_name": "HP Deskjet 2600",
                    "printer_id": "2520979"
                }
            ],
            features=[
                {
                    "feature_name": "Printing colours",
                    "feature_value": "Black"
                },
                {
                    "feature_name": "Black ink volume",
                    "feature_value": "5.5 ml"
                },
                {
                    "feature_name": "Black ink page yield",
                    "feature_value": "300 pages"
                },
            ],
            keywords=["N9K08AE"],
        )

    def test_get_all_products(self):
        response = self.client.get(self.all_products_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_get_searched_products(self):
        response = self.client.get(self.all_products_url + '?q=')
        self.assertRedirects('/products/')
