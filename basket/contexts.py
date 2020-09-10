"""
Shopping basket context processor
"""
from django.conf import settings
from decimal import Decimal


def basket_contents(request):
    basket_items = []
    sub_total = 0

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = settings.DELIVERY_CHARGE
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    basket_total = sub_total + delivery

    context = {
        'basket_items': basket_items,
        'sub_total': sub_total,
        'delivery': delivery,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'free_delivery_delta': free_delivery_delta,
        'basket_total': basket_total,
    }

    return context
