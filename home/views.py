from django.shortcuts import render
from allauth.account.forms import LoginForm, SignupForm


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
