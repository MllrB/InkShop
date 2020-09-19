"""
Shopping basket context processor
"""
from django.conf import settings
from django.shortcuts import get_object_or_404
from decimal import Decimal

from products.models import Supplies
from products.product_functions import get_product_features_info, get_related_products


def basket_contents(request):
    basket_items = []
    sub_total = 0
    total_vat = 0
    basket_total = 0
    product_list = []

    basket = request.session.get('basket', {})

    for item, quantity in basket.items():
        product = get_object_or_404(Supplies, pk=item)
        sub_total += quantity * product.price
        total_vat += (product.calculate_inc_vat_price() -
                      product.price) * quantity
        product_list.append(product)
        basket_items.append({
            'id': item,
            'quantity': quantity,
            'product': product,
        })

    related_products = get_related_products(product_list)
    # remove products already in the basket
    for index, product in enumerate(related_products):
        for item in basket_items:
            if int(item['id']) == int(product.id):
                related_products.pop(index)

    related_products_info = get_product_features_info(related_products)

    if sub_total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = settings.DELIVERY_CHARGE
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - sub_total
    else:
        delivery = 0
        free_delivery_delta = 0

    # not including delivery charge unless items have been added to basket
    if sub_total > 0:
        basket_total = sub_total + total_vat + delivery
        basket_total = round(basket_total, 2)
    else:
        basket_total = 0

    context = {
        'basket_items': basket_items,
        'related_products': related_products,
        'product_info': related_products_info['products_info'],
        'sub_total': sub_total,
        'delivery': delivery,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'free_delivery_delta': free_delivery_delta,
        'total_vat': total_vat,
        'basket_total': basket_total,
    }

    return context
