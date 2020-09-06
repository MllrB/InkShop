"""
Automated testing for products.models
"""
from django.test import TestCase
from decimal import Decimal
from .models import Category, ProductGroup, VatGroup, Supplies


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

    def test_supplies_string_method_returns_supplies_name(self):
        product_group = ProductGroup.objects.create(name="Test ProductGroup")
        vat_group = VatGroup.objects.create(name="Test VatGroup")
        supplies = Supplies.objects.create(name="Test Supplies")
        self.assertEqual(str(supplies), "Test Supplies")

    def test_supplies_calculate_price_method(self):
        product_group = ProductGroup.objects.create(
            name="Test ProductGroup", profit_margin=30)
        vat_group = VatGroup.objects.create(name="Test VatGroup")
        supplies = Supplies.objects.create(name="Test Supplies", cost_price=10)

        test_price = round(Decimal(10/0.7), 2)
        price = supplies.calculate_price()
        self.assertEqual(price, test_price)

    def test_supplies_calculate_inc_vat_price_method(self):
        product_group = ProductGroup.objects.create(
            name="Test ProductGroup", profit_margin=20)
        vat_group = VatGroup.objects.create(name="Test VatGroup")
        supplies = Supplies.objects.create(name="Test Supplies", cost_price=10)

        supplies.price = round(supplies.calculate_price(), 2)
        inc_vat_price = supplies.calculate_inc_vat_price()
        test_price = round(Decimal(10/0.8*1.21), 2)
        self.assertEqual(inc_vat_price, test_price)
