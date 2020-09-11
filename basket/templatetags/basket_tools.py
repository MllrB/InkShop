"""
Functions used to calculate basket totals and basket line totals
"""

from django import template


register = template.Library()


@register.filter(name="calc_line_total")
def calc_line_total(price, quantity):
    return price * quantity
