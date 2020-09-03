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

    if request.method == 'GET':
        query_terms = request.GET['q']
        if not query_terms:
            messages.error(request, 'What exactly are you looking for?')
            return redirect(reverse('home'))

        queries = Q(skus__icontains=query_terms) | Q(
            name__icontains=query_terms) | Q(keywords__icontains=query_terms) | Q(title__contains=query_terms)

        products = products.filter(queries)

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)
