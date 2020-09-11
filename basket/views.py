"""
Views to show the user's shopping basket
"""
from django.shortcuts import render, redirect, reverse

from products.models import Supplies
from products.views import all_products, product_detail


def show_basket(request):
    """ A view that renders the basket page """

    return render(request, 'basket/basket.html')


def add_to_basket(request, product_id):
    """ Adds a quantity of a selected product to the shopping basket """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')

    basket = request.session.get('basket', {})

    if product_id in list(basket.keys()):
        basket[product_id] += quantity
    else:
        basket[product_id] = quantity

    request.session['basket'] = basket
    print(request.session['basket'])

    if 'q' in request.POST:
        request.GET = request.GET.copy()
        request.GET['q'] = request.POST['q']
        return all_products(request)

    return product_detail(request, product_id)


def update_basket(request, product_id):
    new_quantity = int(request.POST.get('quantity'))
    basket = request.session.get('basket', {})
    print(basket)
    if new_quantity > 0:
        basket[product_id] = new_quantity
    else:
        basket.pop(product_id)

    request.session['basket'] = basket

    return redirect(reverse('show_basket'))
