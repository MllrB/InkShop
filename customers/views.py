"""
Customer views
"""
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from allauth.socialaccount.models import SocialAccount
from django.dispatch import receiver

from .models import UserProfile, DeliveryAddress
from .forms import UserProfileForm, UserDeliveryAddressForm


def show_profile(request, template_target):
    this_user = request.user

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
        try:
            delivery_address = get_object_or_404(
                DeliveryAddress, user=user_profile)
        except:
            delivery_address = DeliveryAddress(user=user_profile)

        if request.method == 'POST':
            form = UserDeliveryAddressForm(
                request.POST, instance=delivery_address)
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Delivery address successfully updated')
            else:
                messages.error(
                    request, 'Something went wrong. Please ensure your form is valid')
        else:
            form = UserDeliveryAddressForm(instance=delivery_address)
    else:
        form = UserProfileForm(instance=user_profile)

    email = request.user.email

    print(form)
    context = {
        'form': form,
        'email': email,
        'user': this_user,
        'target': template_target,
    }

    return render(request, 'customers/profile.html', context)
