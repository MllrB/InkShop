from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

from .forms import OrderForm
from customers.forms import UserProfileForm, UserDeliveryAddressForm
from customers.models import UserProfile, DeliveryAddress


def checkout(request):
    """
    A view to return the checkout by card page
    """

    basket = request.session.get('basket', {})

    if not basket:
        messages.error(request, 'There are no products in your basket')
        return redirect(reverse, 'show_basket')

    this_user = request.user
    required_address = None
    delivery_form = None
    delivery_forms = []
    if this_user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=this_user)
        order_form = UserProfileForm(instance=user_profile)

        delivery_addresses = DeliveryAddress.objects.all().filter(user=user_profile)

        if request.method == 'POST':
            required_address = request.POST['delivery']
            if required_address == 'None':
                required_address = None
                delivery_form = UserDeliveryAddressForm()
            else:
                address = get_object_or_404(
                    DeliveryAddress, address_ref=required_address, user=user_profile)
                delivery_form = UserDeliveryAddressForm(instance=address)
        else:
            delivery_form = UserDeliveryAddressForm()
    else:
        order_form = OrderForm()

    context = {
        'form': order_form,
        'delivery_addresses': delivery_addresses,
        'delivery_form': delivery_form,
        'ref': required_address,
    }

    return render(request, 'checkout/checkout.html', context)
