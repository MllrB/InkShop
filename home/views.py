from django.shortcuts import render
from allauth.account.forms import LoginForm, SignupForm

from products.models import Product, Category


def index(request):
    """ 
    A view to render the index page template
    """
    return render(request, 'home/index.html')


def login(request):
    """
    A view to render the login page
    """
    login_form = LoginForm()
    signup_form = SignupForm()

    context = {
        'login_form': login_form,
        'signup_form': signup_form,
    }

    return render(request, 'login.html', context)


def get_categories(request, category):
    """
    A view to return categories that contain printers
    """
    categories = Category.objects.filter(relevant_model=category.lower())

    context = {
        'categories': categories,
        'title': category,
    }

    return render(request, 'home/categories.html', context)


def show_about_us(request):
    """
    A view to render the 'about us' page
    """
    return render(request, 'home/about.html')


def show_delivery_info(request):
    """
    A view to render the 'delivery info' page
    """
    return render(request, 'home/delivery_info.html')


def show_faqs(request):
    """
    A view to render the 'FAQs' page
    """
    return render(request, 'home/faqs.html')


def show_terms(request):
    """
    A view to render the 'Ts & Cs' page
    """
    return render(request, 'home/terms_and_conditions.html')


def show_privacy_policy(request):
    """
    A view to render the 'privacy policy' page
    """
    return render(request, 'home/privacy_policy.html')
