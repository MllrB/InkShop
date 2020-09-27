"""
Allow category info to be used by navigation
"""

from .models import Category


def categories(request):
    """
    Provides nav items category information
    """

    printers = Category.objects.filter(relevant_model='printers')
    supplies = Category.objects.filter(relevant_model='supplies')
    accessories = Category.objects.filter(relevant_model='accessories')

    context = {
        'printers': printers,
        'supplies': supplies,
        'accessories': accessories,
    }

    return context
