"""
Customer Profile views
"""
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from django.dispatch import receiver

from .models import UserProfile, DeliveryAddress
from .forms import UserProfileForm, UserDeliveryAddressForm


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

    try:
        user_profile = get_object_or_404(UserProfile, user=this_user)
    except:
        user_profile = UserProfile(user=this_user)

    if template_target == 'billing':
        if request.method == 'POST':
            form = UserProfileForm(request.POST, instance=user_profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile successfully updated')
            else:
                messages.error(
                    request, 'Something went wrong. Please ensure your form is valid')
        else:
            form = UserProfileForm(instance=user_profile)
    elif template_target == 'delivery':
        delivery_addresses = DeliveryAddress.objects.all().filter(user=user_profile)
        form = None
        if request.method == 'POST':
            if 'updating' in request.POST:
                address_id = int(request.POST['updating'])
                delivery_address = DeliveryAddress.objects.get(pk=address_id)
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

    else:
        form = UserProfileForm(instance=user_profile)

    email = request.user.email

    context = {
        'form': form,
        'email': email,
        'user': this_user,
        'delivery_addresses': delivery_addresses,
        'target': template_target,
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
    this_user = request.user
    email = request.user.email

    delivery_address = DeliveryAddress.objects.get(pk=address_id)
    try:
        delivery_address.delete()
        messages.success(
            request, 'Delivery address successfully removed')
    except:
        messages.error(
            request, 'We were unable to delete that delivery address, please refresh the page and try again')

    try:
        user_profile = get_object_or_404(UserProfile, user=this_user)
    except:
        user_profile = UserProfile(user=this_user)

    delivery_addresses = DeliveryAddress.objects.all().filter(user=user_profile)

    context = {
        'form': None,
        'email': email,
        'user': this_user,
        'delivery_addresses': delivery_addresses,
        'target': template_target,
    }

    return render(request, 'customers/profile.html', context)
