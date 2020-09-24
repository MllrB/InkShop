"""
Automated testing for products.models
"""
from django.test import TestCase
from decimal import Decimal
from .models import Category, ProductGroup, VatGroup, Product


class TestModels(TestCase):

    def test_category_string_method_returns_category_name(self):
        category = Category.objects.create(name="Test Category")
        self.assertEqual(str(category), "Test Category")

    def test_product_group_string_method_returns_product_group_name(self):
        product_group = ProductGroup.objects.create(name="Test ProductGroup")
        self.assertEqual(str(product_group), "Test ProductGroup")

    def test_vat_group_string_method_returns_vat_group_name(self):
        vat_group = VatGroup.objects.create(name="Test VatGroup")
        self.assertEqual(str(vat_group), "Test VatGroup")

    def test_Product_string_method_returns_Product_name(self):
        product_group = ProductGroup.objects.create(name="Test ProductGroup")
        vat_group = VatGroup.objects.create(name="Test VatGroup")
        product = Product.objects.create(name="Test Product")
        self.assertEqual(str(Product), "Test Product")

    def test_Product_calculate_price_method(self):
        product_group = ProductGroup.objects.create(
            name="Test ProductGroup", profit_margin=30)
        vat_group = VatGroup.objects.create(name="Test VatGroup")
        product = Product.objects.create(name="Test Product", cost_price=10)

        test_price = round(Decimal(10/0.7), 2)
        price = product.calculate_price()
        self.assertEqual(price, test_price)

    def test_Product_calculate_inc_vat_price_method(self):
        product_group = ProductGroup.objects.create(
            name="Test ProductGroup", profit_margin=20)
        vat_group = VatGroup.objects.create(name="Test VatGroup")
        product = Product.objects.create(name="Test Product", cost_price=10)

        product.price = round(product.calculate_price(), 2)
        inc_vat_price = product.calculate_inc_vat_price()
        test_price = round(Decimal(10/0.8*1.21), 2)
        self.assertEqual(inc_vat_price, test_price)
