from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Supplies

# Create your views here.


def all_products(request):
    """ 
    A view to return all products and filter results for user searches
    """
    products = Supplies.objects.all()
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
