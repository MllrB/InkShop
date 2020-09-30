from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.forms import formset_factory, modelformset_factory

from .forms import OrderForm
from .models import OrderItem, Order
from customers.forms import UserProfileForm, UserDeliveryAddressForm
from customers.models import UserProfile, DeliveryAddress
from basket.contexts import basket_contents
from products.models import Product

import stripe
import json


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'basket': json.dumps(request.session.get('basket', {})),
            'username': request.user,
            'address_ref': request.POST.get('address_ref')
        })

        request.session['delivery_address_ref'] = request.POST.get(
            'address_ref')
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Sorry, your payment cannot be \
            processed right now. Please try again later.error: {e}')
        return HttpResponse(content=e, status=400)


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

    DeliveryFormSet = modelformset_factory(
        DeliveryAddress, UserDeliveryAddressForm)

    if this_user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=this_user)
        order_form = UserProfileForm(instance=user_profile)

        if request.method == 'POST':
            # save any changes or new addresses authenticated user has made
            my_formset = DeliveryFormSet(
                request.POST, request.FILES)
            if my_formset.is_valid():
                for form in my_formset.forms:
                    form = form.save(commit=False)
                    if form.address_ref == '':
                        continue
                    else:
                        form.address_ref = form.address_ref.replace(' ', '-')
                        form.user = user_profile
                        form.save()
            else:
                messages.error(
                    request, 'One of your forms is invalid, please check and try again')

            if 'delivery_address_ref' in request.session:
                address_ref = request.session.get(
                    'delivery_address_ref', 'None')

            order_delivery_address = get_object_or_404(
                DeliveryAddress, user=user_profile, address_ref=address_ref)

            form_data = {
                'customer_name': order_delivery_address.contact_name,
                'email': user_profile.email,
                'phone_number': order_delivery_address.contact_phone_number,
                'order_address_line1': order_delivery_address.address_line1,
                'order_address_line2': order_delivery_address.address_line2,
                'order_town_or_city': order_delivery_address.town_or_city,
                'order_county': order_delivery_address.county,
                'order_country': order_delivery_address.country,
                'order_post_code': order_delivery_address.post_code,
            }
            order_form = OrderForm(form_data)

            if order_form.is_valid():
                order = order_form.save(commit=False)
                order.user_profile = user_profile
                order.payment_processor = 'Stripe'
                client_secret = request.POST.get(
                    'client_secret').split('_secret')[0]
                order.payment_id = client_secret
                order.original_basket = json.dumps(basket)
                order.save()

                favourites = []
                for item_id, item_qty in basket.items():
                    try:
                        product = get_object_or_404(Product, pk=item_id)
                        order_line = OrderItem(
                            order=order,
                            product=product,
                            quantity=item_qty,
                        )
                        order_line.save()
                        # add purchased products to user favourites
                        if not user_profile.favourites:
                            favourites.append(int(product.id))
                            user_profile.favourites = json.dumps(favourites)
                            user_profile.save()
                        else:
                            favourites = json.loads(user_profile.favourites)
                            favourites.append(int(product.id))
                            favourites = list(dict.fromkeys(favourites))
                            user_profile.favourites = json.dumps(favourites)
                            user_profile.save()
                    except Product.DoesNotExist:
                        messages.error(
                            request, 'One of the products in your basket no longer exists in our catalogue. \
                                please empty your basket and try again')
                        order.delete()
                        return redirect(reverse('show_basket'))

                return redirect(reverse('checkout_success', args=[order.order_number]))
            else:
                messages.error(
                    request, 'There was an error in your form. Please check and try again')

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
                order.payment_processor = 'Stripe'
                client_secret = request.POST.get(
                    'client_secret').split('_secret')[0]
                order.payment_id = client_secret
                order.original_basket = json.dumps(basket)
                order.save()

                for item_id, item_qty in basket.items():
                    try:
                        product = get_object_or_404(Product, pk=item_id)
                        order_line = OrderItem(
                            order=order,
                            product=product,
                            quantity=item_qty,
                        )
                        order_line.save()
                    except Product.DoesNotExist:
                        messages.error(
                            request, 'One of the products in your basket no longer exists in our catalogue. \
                                please empty your basket and try again')
                        order.delete()
                        return redirect(reverse('show_basket'))
                return redirect(reverse('checkout_success', args=[order.order_number]))
            else:
                messages.error(
                    request, 'There was an error in your form. Please check and try again')

        order_form = OrderForm()

    context = {
        'form': order_form,
        'delivery_addresses': delivery_addresses,
        'delivery_forms': delivery_address_forms,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_no):
    """
    Succesful Checkout
    """
    try:
        user_profile = get_object_or_404(UserProfile, user=request.user)
    except:
        user_profile = request.user

    order = get_object_or_404(Order, order_number=order_no)
    messages.success(request, f'Thank you for your order. \
        \nYour order number is {order.order_number}. \
        \nAn email confirmation will be sent to {order.email} momentarily')

    if 'basket' in request.session:
        del request.session['basket']

    context = {
        'order': order,
        'user_profile': user_profile,
    }
    return render(request, 'checkout/checkout_success.html', context)
