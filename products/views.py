import json
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Supplies, ProductGroup, VatGroup, Category
from customers.models import UserProfile
from .product_functions import get_product_features_info, get_related_products

# Create your views here.


def all_products(request):
    """
    A view to return all products and filter results for user searches
    """
    queried_products = Supplies.objects.all().filter(published=True)
    user_search = None
    info_and_filters = {'products_info': None, 'product_filters': None}

    if request.method == 'GET' or request.method == 'POST':
        if 'q' in request.GET:
            user_search = request.GET['q']
            if not user_search:
                messages.warning(
                    request, 'We suggest you try refining your search.')
                return redirect(reverse('products'))

            queries = Q(skus__icontains=user_search) | Q(
                name__icontains=user_search) | Q(keywords__icontains=user_search) | Q(title__icontains=user_search)

            queried_products = queried_products.filter(queries)

            info_and_filters = get_product_features_info(queried_products)

    context = {
        'products': queried_products,
        'search': user_search,
        'product_info': info_and_filters['products_info'],
        'filters': info_and_filters['product_filters'],
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to display individual products and their related products"""

    product = get_object_or_404(Supplies, pk=product_id)

    related_products = get_related_products([product])

    product_info = get_product_features_info([product])
    related_products_info = get_product_features_info(related_products)

    product_features = [product_info['products_info'][0]]
    for x in related_products_info['products_info']:
        product_features.append(x)

    context = {
        'product': product,
        'product_info': product_features,
        'related_products': related_products,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_to_favourites(request, product_id):
    """
    A view to add a product from a user's favourites
    and return the user to the same page
    """
    this_user = request.user

    try:
        user_profile = get_object_or_404(UserProfile, user=this_user)
    except:
        user_profile = UserProfile(user=this_user)
        messages.error(request, 'User not found')

    product = get_object_or_404(Supplies, pk=product_id)
    favourites = []

    if not user_profile.favourites:
        favourites.append(int(product_id))
        favourites = json.dumps(favourites)
        user_profile.favourites = favourites
        user_profile.save()
    else:
        favourites = json.loads(user_profile.favourites)
        favourites.append(int(product_id))
        favourites = list(dict.fromkeys(favourites))
        favourites = json.dumps(favourites)
        user_profile.favourites = favourites
        user_profile.save()

    messages.success(request, f'Added {product.title} to your favourites')

    if 'q' in request.POST:
        request.GET = request.GET.copy()
        request.GET['q'] = request.POST['q']
        return all_products(request)
    elif 'origin' in request.POST:
        if request.POST['origin'] == 'basket':
            return redirect(reverse('show_basket'))
        else:
            product_id = request.POST['origin']
            return product_detail(request, product_id)
    else:
        return product_detail(request, product_id)


@login_required
def remove_from_favourites(request, product_id):
    """
    A view to remove a product from a user's favourites
    and return the user to the same page
    """
    this_user = request.user

    try:
        user_profile = get_object_or_404(UserProfile, user=this_user)
    except:
        user_profile = UserProfile(user=this_user)
        messages.error(request, 'User not found')

    product = get_object_or_404(Supplies, pk=product_id)
    favourites = []

    favourites = json.loads(user_profile.favourites)
    favourites.remove(int(product_id))
    favourites = json.dumps(favourites)
    user_profile.favourites = favourites
    user_profile.save()

    messages.success(request, f'Removed {product.title} from your favourites')

    if 'q' in request.POST:
        request.GET = request.GET.copy()
        request.GET['q'] = request.POST['q']
        return all_products(request)
    elif 'origin' in request.POST:
        if request.POST['origin'] == 'basket':
            return redirect(reverse('show_basket'))
        else:
            product_id = request.POST['origin']
            return product_detail(request, product_id)
    else:
        return product_detail(request, product_id)


@login_required
def product_maintenance(request):
    """
    Returns a template for superusers to perform product maintenance
    """
    if not request.user.is_superuser:
        messages.error(
            request, 'You are not authorised to access this area of the site')
        return redirect(reverse('home'))

    pgroups = ProductGroup.objects.all()
    vatgroups = VatGroup.objects.all()
    categories = Category.objects.all()

    context = {
        'pgroups': pgroups,
        'vatgroups': vatgroups,
        'categories': categories,
    }

    return render(request, 'products/product_maintenance.html', context)


@login_required
def edit_products(request):
    """
    Returns a list of products to edit
    """
    if not request.user.is_superuser:
        messages.error(
            request, 'You are not authorised to access this area of the site')
        return redirect(reverse('home'))

    products = None
    if request.method == 'GET':
        user_search = request.GET['q']
        print(user_search)
        queries = Q(skus__icontains=user_search) | Q(
            name__icontains=user_search) | Q(keywords__icontains=user_search) | Q(title__icontains=user_search)
        products = Supplies.objects.filter(queries)
        print(products.count())
        if products.count() < 1:
            print("none found")

    context = {
        'products': products,
    }

    return render(request, 'products/edit_products.html', context)


@login_required
def update_product_group(request, group_id):
    """
    Updates existing product groups
    """
    if not request.user.is_superuser:
        messages.error(
            request, 'You are not authorised to access this area of the site')
        return redirect(reverse('home'))

    try:
        if request.method == 'POST':
            new_name = request.POST[f'{group_id}_name']
            new_margin = int(request.POST[f'{group_id}_margin'])
            group = get_object_or_404(ProductGroup, pk=group_id)
            group.name = new_name
            group.profit_margin = new_margin
            group.save()
            messages.success(request, 'Product group updated')
    except:
        messages.error(request, 'Unable to update product group')

    return redirect(reverse('product_maintenance'))


@login_required
def update_vat_group(request, group_id):
    """
    Updates existing vat groups
    """
    if not request.user.is_superuser:
        messages.error(
            request, 'You are not authorised to access this area of the site')
        return redirect(reverse('home'))

    try:
        if request.method == 'POST':
            new_name = request.POST[f'{group_id}_name']
            new_rate = int(request.POST[f'{group_id}_rate'])
            group = get_object_or_404(VatGroup, pk=group_id)
            group.name = new_name
            group.vat_rate = new_rate
            group.save()
            messages.success(request, 'Product group updated')
    except:
        messages.error(request, 'Unable to update product group')

    return redirect(reverse('product_maintenance'))


@login_required
def update_category(request, category_id):
    """
    Updates existing vat groups
    """
    if not request.user.is_superuser:
        messages.error(
            request, 'You are not authorised to access this area of the site')
        return redirect(reverse('home'))

    try:
        if request.method == 'POST':
            new_name = request.POST[f'{category_id}_name']
            new_description = request.POST[f'{category_id}_description']
            category = get_object_or_404(Category, pk=category_id)
            category.friendly_name = new_name
            category.description = new_description

            new_name = new_name.replace(' ', '_')
            category.name = new_name.lower()

            category.save()
            messages.success(request, 'Category updated')
    except:
        messages.error(request, 'Unable to update product group')

    return redirect(reverse('product_maintenance'))


@login_required
def update_prices(request):
    """
    Updates all product prices
    """
    if not request.user.is_superuser:
        messages.error(
            request, 'You are not authorised to access this area of the site')
        return redirect(reverse('home'))

    try:
        all_products = Supplies.objects.all()
        for product in all_products:
            product_to_update = get_object_or_404(Supplies, pk=product.id)
            product_to_update.price = product_to_update.calculate_price()
            product_to_update.save()

        messages.success(request, 'Product prices updated')
    except:
        messages.error(request, 'Unable to update all products')

    return redirect(reverse('product_maintenance'))
