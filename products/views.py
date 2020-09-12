from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Supplies
from .product_functions import get_product_features_info, get_related_products

# Create your views here.


def all_products(request):
    """ 
    A view to return all products and filter results for user searches
    """
    queried_products = Supplies.objects.all().filter(published=True)
    user_search = None
    product_info = []
    product_filters = []
    products = []

    if request.method == 'GET' or request.method == 'POST':
        if 'q' in request.GET:
            user_search = request.GET['q']
            if not user_search:
                messages.error(request, 'What exactly are you looking for?')
                return redirect(reverse('products'))

            queries = Q(skus__icontains=user_search) | Q(
                name__icontains=user_search) | Q(keywords__icontains=user_search) | Q(title__contains=user_search)

            queried_products = queried_products.filter(queries)

            info_and_filters = get_product_features_info(products)

    context = {
        'products': queried_products,
        'search': user_search,
        'product_info': info_and_filters['products_info'],
        'filters': info_and_filters['product_filters'],
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to display individual products and their related products"""
    product = get_object_or_404(Supplies, pk=product_id)

    related_products = get_related_products([product])

    product_info = get_product_features_info([product])
    related_products_info = get_product_features_info(related_products)

    product_features = [product_info['products_info'][0]]
    for x in related_products_info['products_info']:
        product_features.append(x)

    context = {
        'product': product,
        'product_info': product_features,
        'related_products': related_products,
    }

    return render(request, 'products/product_detail.html', context)
