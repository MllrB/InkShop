from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Supplies

# Create your views here.


def all_products(request):
    """ 
    A view to return all products and filter results for user searches
    """
    products = Supplies.objects.all().filter(published=True)
    user_search = None
    product_info = []
    product_filters = []

    if request.method == 'GET':
        user_search = request.GET['q']
        if not user_search:
            messages.error(request, 'What exactly are you looking for?')
            return redirect(reverse('home'))

        queries = Q(skus__icontains=user_search) | Q(
            name__icontains=user_search) | Q(keywords__icontains=user_search) | Q(title__contains=user_search)

        products = products.filter(queries)

        for product in products:
            info = {}
            info['id'] = product.id
            for feature in product.features:
                if 'yield' in feature['feature_name'].lower():
                    if 'footnote' not in feature['feature_name'].lower():
                        info['pages'] = feature['feature_value'].lower()
                if 'colours' in feature['feature_name'].lower():
                    info['colour'] = feature['feature_value'].lower()
                    product_filters.append(feature['feature_value'].lower())
                if 'volume' in feature['feature_name'].lower():
                    info['volume'] = feature['feature_value'].lower()

            product_info.append(info)
        product_filters = list(dict.fromkeys(product_filters))
    context = {
        'products': products,
        'search': user_search,
        'product_info': product_info,
        'filters': product_filters,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to display individual products and their related products"""
    product = get_object_or_404(Supplies, pk=product_id)

    shared_printers = []
    for printer in product.related_printers:
        shared_printers.append(printer['printer_id'])

    print(shared_printers)
    print(len(shared_printers))

    related_matches = []
    for printer_id in shared_printers:
        query = Q(related_printers__contains=printer_id)
        related_matches.append(Supplies.objects.filter(
            query).exclude(pk=product_id))

    matched_ids = []
    for queryset in related_matches:
        for query_obj in queryset:
            matched_ids.append(query_obj.id)
    matched_ids = list(dict.fromkeys(matched_ids))
    print(matched_ids)

    related_products = []
    for related_id in matched_ids:
        related_product = get_object_or_404(Supplies, pk=related_id)
        related_products.append(related_product)

    context = {
        'product': product,
        'related_products': related_products,
    }

    return render(request, 'products/product_detail.html', context)
