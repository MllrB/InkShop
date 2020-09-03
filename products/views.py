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

    if request.method == 'GET':
        user_search = request.GET['q']
        if not user_search:
            messages.error(request, 'What exactly are you looking for?')
            return redirect(reverse('home'))

        queries = Q(skus__icontains=user_search) | Q(
            name__icontains=user_search) | Q(keywords__icontains=user_search) | Q(title__contains=user_search)

        products = products.filter(queries)

    context = {
        'products': products,
        'search': user_search,
    }

    return render(request, 'products/products.html', context)
