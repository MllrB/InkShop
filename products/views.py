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

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)
