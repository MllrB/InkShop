"""
Checkout Models
"""
import uuid
from django.db import models
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from customers.models import UserProfile, DeliveryAddress
from products.models import Product


class Order(models.Model):
    order_number = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='orders')
    date = models.DateTimeField(auto_now_add=True)

    customer_name = models.CharField(max_length=60, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    order_address_line1 = models.CharField(
        max_length=180, null=False, blank=False)
    order_address_line2 = models.CharField(
        max_length=180, null=True, blank=True)
    order_town_or_city = models.CharField(
        max_length=180, null=True, blank=True)
    order_county = models.CharField(max_length=180, null=True, blank=True)
    order_country = CountryField(
        blank_label='Country', null=False, blank=False)
    order_post_code = models.CharField(max_length=8, null=True, blank=True)

    order_subtotal = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    order_VAT = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)

    payment_processor = models.CharField(
        max_length=60, null=False, blank=False, default='')
    payment_id = models.CharField(
        max_length=254, null=False, blank=False, default='')

    original_basket = models.TextField(null=False, blank=False, default='')

    def update_total(self):
        """
        Update order totals and delivery cost each time a 
        product is added or removed
        """
        self.order_subtotal = self.order_items.aggregate(
            Sum('total_price'))['total_price__sum'] or 0
        self.order_VAT = self.order_items.aggregate(
            Sum('total_VAT'))['total_VAT__sum'] or 0

        if self.order_subtotal < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = settings.DELIVERY_CHARGE
        else:
            self.delivery_cost = 0

        self.grand_total = self.order_subtotal + self.order_VAT + self.delivery_cost
        self.save()

    def __str__(self):
        return str(self.order_number)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE, related_name='order_items')
    product_model_name = models.CharField(
        max_length=60, null=False, blank=False, default="Supplies")
    product_id = models.CharField(
        max_length=60, null=False, blank=False, default='')
    quantity = models.IntegerField(null=False, blank=False, default=0)
    total_VAT = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    total_price = models.DecimalField(
        max_digits=3, decimal_places=2, null=False, blank=False, editable=False, default=0)

    def save(self, *args, **kwargs):
        """
        Overide save method to update the VAT and Price totals and
        save the product
        """
        if self.product_model_name == 'Supplies':
            product = models.ForeignKey(
                Product, null=False, blank=False, on_delete=models.CASCADE)
            self.product = get_object_or_404(Product, pk=self.product_id)
            self.total_price = self.product.price * self.quantity
            self.total_VAT = self.product.calculate_vat() * self.quantity

        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU: {self.product_id} in Order No. {self.order.order_number}'
