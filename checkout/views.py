from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.forms import formset_factory, modelformset_factory

from .forms import OrderForm
from customers.forms import UserProfileForm, UserDeliveryAddressForm
from customers.models import UserProfile, DeliveryAddress
from basket.contexts import basket_contents

import stripe


def checkout(request):
    """
    A view to return the checkout by card page
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    basket = request.session.get('basket', {})

    if not basket:
        messages.error(request, 'There are no products in your basket')
        return redirect(reverse, 'show_basket')

    # stripe
    current_basket = basket_contents(request)
    total = current_basket['basket_total']
    stripe_total = round(total*100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    this_user = request.user
    delivery_form = UserDeliveryAddressForm()
    delivery_addresses = None
    delivery_address_forms = [delivery_form]

    if this_user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=this_user)
        order_form = UserProfileForm(instance=user_profile)

        DeliveryFormSet = modelformset_factory(
            DeliveryAddress, UserDeliveryAddressForm)

        if request.method == 'POST':
            my_formset = DeliveryFormSet(
                request.POST, request.FILES)
            if my_formset.is_valid():
                for form in my_formset.forms:
                    form = form.save(commit=False)
                    form.address_ref = form.address_ref.replace(' ', '-')
                    form.user = user_profile
                    form.save()
            else:
                messages.error(request, my_formset.errors)

        delivery_addresses = DeliveryAddress.objects.filter(user=user_profile)
        delivery_address_forms = DeliveryFormSet(
            queryset=delivery_addresses)
        print(delivery_address_forms.errors)
    else:
        order_form = OrderForm()

    context = {
        'form': order_form,
        'delivery_addresses': delivery_addresses,
        'delivery_forms': delivery_address_forms,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, 'checkout/checkout.html', context)


def checkout_success(request):
    return render(request, 'checkout/checkout_success.html')
