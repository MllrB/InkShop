"""
Customer views
"""
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from allauth.socialaccount.models import SocialAccount
from django.dispatch import receiver

from .models import UserProfile, DeliveryAddress
from .forms import UserProfileForm, UserDeliveryAddressForm


def show_profile(request, template_target):
    this_user = request.user
    user_id = request.user.id
    delivery_addresses = None

    try:
        user_profile = get_object_or_404(UserProfile, user=this_user)
    except:
        user_profile = UserProfile(user=this_user)

    print('in view')
    print(user_profile)

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


def add_delivery_address(request, template_target):
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


def edit_delivery_address(request, template_target):
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
