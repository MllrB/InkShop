"""
Views to show the user's shopping basket
"""
from django.shortcuts import render


def show_basket(request):
    return render(request, 'basket/basket.html')
