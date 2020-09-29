""" 
Functions for building product info and finding related products
"""

from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Product, Category


def get_product_features_info(products):
    """ build product features and filter info dictionaries """
    products_info = []
    product_filters = []
    for product in products:
        info = {}
        info['id'] = product.id
        category = get_object_or_404(Category, pk=product.category.id)
        if category.relevant_model == 'supplies':
            for feature in product.features:
                if 'yield' in feature['feature_name'].lower():
                    if 'footnote' not in feature['feature_name'].lower():
                        info['pages'] = feature['feature_value'].lower()
                if 'colours' in feature['feature_name'].lower():
                    info['colour'] = feature['feature_value'].lower()
                    product_filters.append(
                        feature['feature_value'].lower())
                if 'volume' in feature['feature_name'].lower():
                    info['volume'] = feature['feature_value'].lower()
        elif category.relevant_model == 'printers':
            for feature in product.features:
                if 'print technology' in feature['feature_name'].lower():
                    info['print_tech'] = feature['feature_value'].lower()
                if 'print speed' in feature['feature_name'].lower():
                    info['print_speed'] = feature['feature_value'].lower()
                if 'color printing' in feature['feature_value'].lower():
                    info['print_colour'] = feature['feature_value'].lower()
                    product_filters.append(
                        feature['feature_value'].lower())
                if 'mono printing' in feature['feature_value'].lower():
                    info['print_colour'] = feature['feature_value'].lower()
                    product_filters.append(
                        feature['feature_value'].lower())
        elif category.relevant_model == 'accessories':
            for feature in product.features:
                if 'paper size' in feature['feature_name'].lower():
                    info['paper_size'] = feature['feature_value'].lower()
                    product_filters.append(
                        feature['feature_value'].lower())
                if 'sheets' in feature['feature_name'].lower():
                    info['sheets'] = feature['feature_value'].lower()
                if 'media weight' in feature['feature_name'].lower():
                    info['media_weight'] = feature['feature_value'].lower()
                if 'capacity' in feature['feature_name'].lower():
                    info['capacity'] = feature['feature_value'].lower()
                    product_filters.append(
                        feature['feature_value'].lower())
                if 'interface' in feature['feature_name'].lower():
                    info['interface'] = feature['feature_value'].lower()
                if 'usb version' in feature['feature_name'].lower():
                    info['usb'] = feature['feature_value'].lower()

        products_info.append(info)

    product_filters = list(dict.fromkeys(product_filters))

    return {'products_info': products_info, 'product_filters': product_filters}


def get_related_products(products):
    """ 
    find products related by common printers 
    Accepts a list as an argument
    """
    # Finding all related products by shared printers
    shared_printers = []
    related_matches = []
    for product in products:

        for printer in product.related_printers:
            shared_printers.append(printer['printer_id'])

        for printer_id in shared_printers:
            query = Q(related_printers__contains=printer_id)
            related_matches.append(Product.objects.filter(
                query).exclude(pk=product.id))

    # reducing the list to unique matches
    matched_ids = []
    for queryset in related_matches:
        for query_obj in queryset:
            matched_ids.append(query_obj.id)
    matched_ids = list(dict.fromkeys(matched_ids))

    related_products = []
    for related_id in matched_ids:
        related_product = get_object_or_404(Product, pk=related_id)
        related_products.append(related_product)

    return related_products
