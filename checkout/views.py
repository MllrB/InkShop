from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.forms import formset_factory, modelformset_factory

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
    delivery_form = UserDeliveryAddressForm()
    delivery_addresses = None
    delivery_address_forms = [delivery_form]

    if this_user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=this_user)
        order_form = UserProfileForm(instance=user_profile)

        DeliveryFormSet = modelformset_factory(
            DeliveryAddress, UserDeliveryAddressForm)
        delivery_address_forms = DeliveryFormSet(
            queryset=DeliveryAddress.objects.filter(user=user_profile))
        total_forms = delivery_address_forms.total_form_count()
        blank_form_id = f'form-{total_forms - 1}'
        blank_form = f'{blank_form_id}-address_ref'
        print(blank_form_id)

        delivery_addresses = DeliveryAddress.objects.filter(user=user_profile)

        if request.method == 'POST':
            print(request.POST)
            if request.POST[blank_form] != '':
                print('wahey!')
                # removing whitespace from address ref
                address_ref_nws = request.POST[blank_form].replace(' ', '_')
                new_delivery_address = DeliveryAddress(
                    user=user_profile,
                    address_ref=address_ref_nws,
                    contact_name=request.POST[f'{blank_form_id}-contact_name'],
                    contact_phone_number=request.POST[f'{blank_form_id}-contact_phone_number'],
                    address_line1=request.POST[f'{blank_form_id}-address_line1'],
                    address_line2=request.POST[f'{blank_form_id}-address_line2'],
                    town_or_city=request.POST[f'{blank_form_id}-town_or_city'],
                    county=request.POST[f'{blank_form_id}-county'],
                    post_code=request.POST[f'{blank_form_id}-post_code'],
                    country=request.POST[f'{blank_form_id}-country'],
                )
                new_delivery_address.save()
    else:
        order_form = OrderForm()

    context = {
        'form': order_form,
        'delivery_addresses': delivery_addresses,
        'delivery_forms': delivery_address_forms,
        'stripe_public_key': 'pk_test_51H4XWiD9PZjek6qFetNbsghsphTJQ8gyyXXLhBQH6CHwskR9t9p77BDpGRKBiLm1CnZybPlzpMOpJAtLfLEayC5g00UrBGbDLM',
        'client_secret': 'Test CS',
    }

    return render(request, 'checkout/checkout.html', context)


def checkout_success(request):
    return render(request, 'checkout/checkout_success.html')
