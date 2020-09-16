"""
User contexts
"""

import json
from django.shortcuts import get_object_or_404
from django.contrib import messages

from customers.models import UserProfile
from products.models import Supplies


def user_favourited_products(request):
    user_favourites = None
    favourited_products = None
    if request.user.is_authenticated:
        try:
            this_user = get_object_or_404(UserProfile, user=request.user)
            user_favourites = json.loads(this_user.favourites)
            favourited_products = Supplies.objects.filter(
                pk__in=user_favourites)
        except:
            this_user = UserProfile(user=request.user)

    context = {
        'favourites': user_favourites,
        'favourite_products': favourited_products,
    }

    return context
