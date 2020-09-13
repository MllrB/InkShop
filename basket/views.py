"""
Views to show the user's shopping basket
"""
from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Supplies
from products.views import all_products, product_detail


def show_basket(request):
    """ A view that renders the basket page """

    return render(request, 'basket/basket.html')


def add_to_basket(request, product_id):
    """ Adds a quantity of a selected product to the shopping basket """

    product = get_object_or_404(Supplies, pk=product_id)
    quantity = int(request.POST.get('quantity'))

    basket = request.session.get('basket', {})

    if product_id in list(basket.keys()):
        basket[product_id] += quantity
        messages.success(
            request, f'The quantity of {product.title} in your basket has been updated.')
    else:
        basket[product_id] = quantity
        messages.success(request, f'Added {product.title} to your basket')

    request.session['basket'] = basket

    if 'q' in request.POST:
        request.GET = request.GET.copy()
        request.GET['q'] = request.POST['q']
        return all_products(request)
    elif 'origin' in request.POST:
        if request.POST['origin'] == 'basket':
            return redirect(reverse('show_basket'))
        else:
            product_id = request.POST['origin']
            return product_detail(request, product_id)
    else:
        return product_detail(request, product_id)


def update_basket(request, product_id):
    """ A view to update line quantities in the basket """

    product = get_object_or_404(Supplies, pk=product_id)
    new_quantity = int(request.POST.get('quantity'))
    basket = request.session.get('basket', {})
    basket[product_id] = new_quantity
    messages.success(
        request, f'The quantity of {product.title} in your basket has been updated')

    request.session['basket'] = basket

    return redirect(reverse('show_basket'))


def remove_from_basket(request, product_id):
    """ A view to remove a product from the shopping basket """
    try:
        product = get_object_or_404(Supplies, pk=product_id)
        basket = request.session.get('basket', {})
        basket.pop(product_id)
        messages.success(
            request, f'{product.title} has been removed from your basket')

        request.session['basket'] = basket
        return HttpResponse(status=200)

    except Exception as oopsie:
        messages.error(
            request, "Something went wrong, could not remove that product from your basket")
        return HttpResponse(status=500)
