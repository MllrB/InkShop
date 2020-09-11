"""
Functions used to calculate basket totals and basket line totals
"""

from django import template
from django.shortcuts import get_object_or_404
from decimal import Decimal

from products.models import Supplies


register = template.Library()


@register.filter(name="calc_line_total")
def calc_line_total(price, quantity):
    return price * quantity


@register.filter(name="calc_total_vat")
def calc_total_vat(basket_items):
    total_vat = 0
    for item in basket_items:
        product = get_object_or_404(Supplies, pk=item['product'].id)
        product_vat = product.calculate_inc_vat_price() - product.price
        total_vat += product_vat * int(item['quantity'])

    return total_vat
