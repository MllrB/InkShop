"""
User contexts
"""

import json
from django.shortcuts import get_object_or_404

from customers.models import UserProfile


def user_favourited_products(request):
    user_favourites = None
    if request.user.is_authenticated:
        this_user = get_object_or_404(UserProfile, user=request.user)
        user_favourites = json.loads(this_user.favourites)

    context = {
        'favourites': user_favourites,
    }

    return context
