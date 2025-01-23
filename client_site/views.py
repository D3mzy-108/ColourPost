from django.shortcuts import render, redirect, get_object_or_404
from manufacturer_site.classifications.models import Product, Packaging, ProductType
from django.db.models import Q


def home(request):
    context = {}
    return render(request, 'client_site/home.html', context)


def store(request):
    package = request.GET.get('pkg') or ''
    product_type = request.GET.get('pty') or ''
    query = request.GET.get('q') or ''
    products = Product.objects.filter(
        Q(product_color__icontains=query) &
        Q(product_type__id__icontains=product_type) &
        Q(package__id__icontains=package)
    ).order_by('?')
    context = {
        'products': products,
        'packaging': Packaging.objects.all(),
        'product_types': ProductType.objects.all(),
        'cart': request.session.get('cart', []),
    }
    return render(request, 'client_site/store.html', context)


def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])
    cart.append(product_id)
    request.session['cart'] = cart
    return redirect(request.META.get('HTTP_REFERER', 'store'))


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])
    if len(cart) > 0:
        cart.remove(product_id)
    request.session['cart'] = cart
    return redirect(request.META.get('HTTP_REFERER', 'checkout'))


def checkout(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(pk__in=cart)
    context = {
        'products': products,
        'cart': cart,
    }
    return render(request, 'client_site/checkout.html', context)
