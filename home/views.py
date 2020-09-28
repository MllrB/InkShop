from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from allauth.account.forms import LoginForm, SignupForm
from django.contrib.auth.decorators import login_required

from .models import ContentManagement
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
    about_content = ContentManagement.objects.get(active=True)
    context = {
        'page_content': about_content.about,
    }
    return render(request, 'home/about.html', context)


def show_delivery_info(request):
    """
    A view to render the 'delivery info' page
    """
    delivery_content = ContentManagement.objects.get(active=True)
    context = {
        'page_content': delivery_content.delivery,
    }
    return render(request, 'home/delivery_info.html', context)


def show_faqs(request):
    """
    A view to render the 'FAQs' page
    """
    faqs_content = ContentManagement.objects.get(active=True)
    context = {
        'page_content': faqs_content.questions,
    }
    return render(request, 'home/faqs.html', context)


def show_terms(request):
    """
    A view to render the 'Ts & Cs' page
    """
    terms_content = ContentManagement.objects.get(active=True)
    context = {
        'page_content': terms_content.terms,
    }
    return render(request, 'home/terms_and_conditions.html', context)


def show_privacy_policy(request):
    """
    A view to render the 'privacy policy' page
    """
    privacy_content = ContentManagement.objects.get(active=True)
    context = {
        'page_content': privacy_content.privacy,
    }
    return render(request, 'home/privacy_policy.html', context)


######################
# CONTENT MANAGEMENT #
######################

@login_required
def content_management(request):
    """
    Returns a template for superusers to perform content management
    """
    if not request.user.is_superuser:
        messages.error(
            request, 'You are not authorised to access this area of the site')
        return redirect(reverse('home'))

    contents = ContentManagement.objects.all()
    content_names = []
    for content in contents:
        content_names.append(content.name)

    context = {
        'saved_content': contents,
        'content_names': content_names,
    }

    return render(request, 'home/content_management.html', context)


def save_content_changes(request):
    """
    Saves user changes to content pages
    """
    if not request.user.is_superuser:
        messages.error(
            request, 'You are not authorised to access this area of the site')
        return redirect(reverse('home'))

    if request.method == 'POST':
        content_id = int(request.POST['content_id'])

        if content_id != 1:
            try:
                content = get_object_or_404(ContentManagement, name='custom')
                content.about = request.POST['about-us-custom']
                content.delivery = request.POST['delivery-info-custom']
                content.questions = request.POST['faqs-custom']
                content.terms = request.POST['terms-conditions-custom']
                content.privacy = request.POST['privacy-policy-custom']
                content.save()
                messages.success(
                    request, "Your changes were saved to 'custom'.")

            except:
                messages.error(
                    request, "Sorry, something wnet wrong and your changes weren't saved. Please try again")
        else:
            try:
                content = get_object_or_404(ContentManagement, name='custom')
                content.about = request.POST['about-us-primary']
                content.delivery = request.POST['delivery-info-primary']
                content.questions = request.POST['faqs-primary']
                content.terms = request.POST['terms-conditions-primary']
                content.privacy = request.POST['privacy-policy-primary']
                content.save()
            except:
                ContentManagement.objects.create(
                    name='custom',
                    about=request.POST['about-us-primary'],
                    delivery=request.POST['delivery-info-primary'],
                    questions=request.POST['faqs-primary'],
                    terms=request.POST['terms-conditions-primary'],
                    privacy=request.POST['privacy-policy-primary']
                )
            messages.success(
                request, "Your changes were saved to a template called 'custom'.")

        print(request.POST)
        content_templates = ContentManagement.objects.all()
        if 'make-active-custom' in request.POST:
            print(True)
            for template in content_templates:
                if template.name == 'custom':
                    template.active = True
                else:
                    template.active = False
                template.save()
        else:
            for template in content_templates:
                if template.name == 'custom':
                    template.active = False
                else:
                    template.active = True
                template.save()

    return redirect(reverse('content_management'))


def recommended_products(request):
    """
    A view to allow staff to select the recommended products on the homepage
    """

    if not request.user.is_superuser:
        messages.error(
            request, 'You are not authorised to access this area of the site')
        return redirect(reverse('home'))

    content_templates = ContentManagement.objects.all()
    context = {
        'content_templates': content_templates,
    }

    return render(request, 'home/recommended_products.html', context)


def find_products_to_recommend(request):
    """
    Finds products from a user search and returns a page that allows the user to select
    which products to add to which ContentManagement record
    """

    if not request.user.is_superuser:
        messages.error(
            request, 'You are not authorised to access this area of the site')
        return redirect(reverse('home'))

    products = None
    if request.method == 'GET':
        user_search = request.GET['q']
        queries = Q(skus__icontains=user_search) | Q(
            title__icontains=user_search) | Q(description__icontains=user_search)
        products = Product.objects.filter(queries)
        if products.count() < 1:
            print("none found")

    context = {
        'products': products,
    }

    return render(request, 'home/products_to_recommend.html', context)


def save_recommended_product(request, product_id):
    """
    Save the changes a user has made to recommended products
    """
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        content_to_update = request.POST['template']
        position = int(request.POST['position'])

        content_template = ContentManagement.objects.get(
            name=content_to_update)
        if position == 1:
            content_template.staff_pick1 = product
        elif position == 2:
            content_template.staff_pick2 = product
        else:
            content_template.staff_pick3 = product

        content_template.save()

    return redirect(reverse('recommended_products'))
