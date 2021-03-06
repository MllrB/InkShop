"""
Customer Profile views
"""
import json
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from django.dispatch import receiver

from .models import UserProfile, DeliveryAddress
from .forms import UserProfileForm, UserDeliveryAddressForm
from checkout.models import Order, OrderItem
from products.models import Product


@login_required
def show_profile(request, template_target):
    """
    A view to show the user's profile

    PARAMS:
    template_target:    A string used to determine which part of their profile a user wishes to see.
                        Options are 'billing', 'delivery', 'favourites and 'orders'.

    """
    this_user = request.user
    delivery_addresses = None
    form = None
    ordered_products = []

    try:
        user_profile = get_object_or_404(UserProfile, user=this_user)
    except:
        user_profile = UserProfile(user=this_user)

    if template_target == 'billing':
        if request.method == 'POST':
            user_profile.email = request.user.email
            user_profile.save()
            form = UserProfileForm(
                request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                form.save(commit=False)
                form.save()
                messages.success(request, 'Profile successfully updated')
            else:
                messages.error(
                    request, 'Something went wrong. Please ensure your form is valid')
            form = UserProfileForm(instance=user_profile)
        else:
            form = UserProfileForm(instance=user_profile)
    elif template_target == 'delivery':
        form = None
        if request.method == 'POST':

            user_profile.email = request.user.email
            user_profile.save()

            if 'updating' in request.POST:
                address_id = int(request.POST['updating'])
                delivery_address = DeliveryAddress.objects.get(
                    pk=address_id)
                form = UserDeliveryAddressForm(
                    request.POST, instance=delivery_address, updating=True)
            else:
                delivery_address = DeliveryAddress(user=user_profile)

                form = UserDeliveryAddressForm(
                    request.POST, instance=delivery_address, user=user_profile)

            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Delivery address successfully updated')
            else:
                messages.error(
                    request, 'Something went wrong. Please ensure your form is valid')
                delivery_addresses = None

        delivery_addresses = DeliveryAddress.objects.all().filter(user=user_profile)
        if not delivery_addresses:
            form = UserDeliveryAddressForm()
    elif template_target == 'orders':
        orders = user_profile.orders.all()
        for order in orders:
            order_line = order.order_items.all()
            for line in order_line:
                product = get_object_or_404(Product, pk=line.product.id)
                ordered_products.append({
                    'order_num': order.order_number,
                    'product': product,
                    'qty': line.quantity,
                })
    email = request.user.email

    context = {
        'form': form,
        'email': email,
        'user': user_profile,
        'delivery_addresses': delivery_addresses,
        'target': template_target,
        'ordered_products': ordered_products,
    }

    return render(request, 'customers/profile.html', context)


@login_required
def add_delivery_address(request, template_target):
    """
    A view for users to add a new delivery address.
    """
    this_user = request.user
    try:
        user_profile = get_object_or_404(UserProfile, user=this_user)
    except:
        user_profile = UserProfile(user=this_user)

    form = UserDeliveryAddressForm(instance=user_profile)
    email = request.user.email

    context = {
        'form': form,
        'email': email,
        'user': this_user,
        'delivery_addresses': None,
        'target': template_target,
    }

    return render(request, 'customers/profile.html', context)


@login_required
def update_delivery_address(request, address_id):
    """
    A view to update a user's saved delivery address.
    """
    template_target = 'delivery'
    this_user = request.user
    delivery_address = DeliveryAddress.objects.get(pk=address_id)

    form = UserDeliveryAddressForm(instance=delivery_address)
    email = request.user.email

    context = {
        'form': form,
        'email': email,
        'user': this_user,
        'delivery_addresses': None,
        'target': template_target,
        'updating': True,
        'address_id': address_id,
    }

    return render(request, 'customers/profile.html', context)


@login_required
def delete_delivery_address(request, address_id):
    """
    A view to delete a user's saved delivery address.
    """

    template_target = 'delivery'

    delivery_address = DeliveryAddress.objects.get(pk=address_id)
    try:
        delivery_address.delete()
        messages.success(
            request, 'Delivery address successfully removed')
        return show_profile(request, template_target)
    except:
        messages.error(
            request, 'We were unable to delete that delivery address, please refresh the page and try again')


@login_required
def delete_favourited_product(request, product_id):
    """
    A view to delete a product from a user's favourites via the user's profile
    """

    template_target = 'favourites'
    user_profile = get_object_or_404(UserProfile, user=request.user)

    try:
        favourites = []
        favourites = json.loads(user_profile.favourites)
        favourites.remove(int(product_id))
        favourites = json.dumps(favourites)
        user_profile.favourites = favourites
        user_profile.save()

        messages.success(
            request, 'Product successfully removed from your favourites')
        return show_profile(request, template_target)
    except Exception as e:
        print(e)
        messages.error(
            request, 'We were unable to delete that product from your favourites, please refresh the page and try again')
        return show_profile(request, template_target)


def repeat_order(request, order_id):
    """
    Adds products from a previous order to a users basket and redirects to the basket page
    """

    order = get_object_or_404(Order, order_number=order_id)
    order_items = order.order_items.all()

    basket = request.session.get('basket', {})

    for item in order_items:
        product_id = str(item.product.id)
        if product_id in list(basket.keys()):
            basket[product_id] += item.quantity
        else:
            basket[product_id] = item.quantity

    messages.success(
        request, 'Products from your previous order have been added to your basket')
    request.session['basket'] = basket

    return redirect(reverse('show_basket'))
