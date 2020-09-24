from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
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
            # save any changes or new addresses authenticated user has made
            my_formset = DeliveryFormSet(
                request.POST, request.FILES)
            if my_formset.is_valid():
                for form in my_formset.forms:
                    form = form.save(commit=False)
                    form.address_ref = form.address_ref.replace(' ', '-')
                    form.user = user_profile
                    form.save()
            else:
                print(my_formset.errors)

            print(request.POST)
            print(intent)

        delivery_addresses = DeliveryAddress.objects.filter(user=user_profile)
        delivery_address_forms = DeliveryFormSet(
            queryset=delivery_addresses)
    else:
        if request.method == 'POST':
            form_data = {
                'customer_name': request.POST['customer_name'],
                'email': request.POST['email'],
                'phone_number': request.POST['phone_number'],
                'order_address_line1': request.POST['order_address_line1'],
                'order_address_line2': request.POST['order_address_line2'],
                'order_town_or_city': request.POST['order_town_or_city'],
                'order_county': request.POST['order_county'],
                'order_country': request.POST['order_country'],
                'order_post_code': request.POST['order_post_code'],
            }
            order_form = OrderForm(form_data)
            if order_form.is_valid():
                order = order_form.save(commit=False)
                # try:
                #     this_user = get_object_or_404(
                #         UserProfile, email=form_data['email'])
                # except:
                #     username = form_data['customer_name'].replace(' ', '')
                #     new_user = User.objects.create_user(
                #         username=username, email=form_data['email'], password=None)
                #     this_user = UserProfile.objects.create(
                #         user=new_user,
                #         full_name=form_data['customer_name'],
                #         email=form_data['email'],
                #         default_phone_number=form_data['email'],
                #         billing_address_line1=form_data['order_address_line1'],
                #         billing_address_line2=form_data['order_address_line2'],
                #         billing_town_or_city=form_data['order_town_or_city'],
                #         billing_county=form_data['order_county'],
                #         billing_post_code=form_data['order_post_code'],
                #         billing_country=form_data['order_country'],
                #     )

                # order.user_profile = this_user
                order.payment_processor = 'Stripe'
                order.payment_id = intent['client_secret'].split('_secret')[0]
                order.original_basket = current_basket
                order.save()

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
