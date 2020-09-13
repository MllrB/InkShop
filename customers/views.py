"""
Customer views
"""
from django.shortcuts import render, get_object_or_404
from allauth.socialaccount import providers

from .models import UserProfile
from .forms import UserProfileForm


def show_profile(request):
    this_user = request.user
    try:
        user_profile = get_object_or_404(UserProfile, user=this_user)
    except:
        user_profile = UserProfile(user=this_user)

    print(this_user)

    form = UserProfileForm(instance=user_profile)
    email = request.user.email
    context = {
        'form': form,
        'email': email,
    }

    return render(request, 'customers/profile.html', context)
