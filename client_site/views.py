from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from manufacturer_site.classifications.models import Product, Packaging, ProductType
from django.db.models import Q
from manufacturer_site.cashier.models import Order, Sale
from manufacturer_site.production.views import _generate_random_string
from django.contrib import messages
# MAIL IMPORTS
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


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
    products = Product.objects.filter(id__in=cart)
    if request.method == 'POST':
        checkout_items = []
        for item in cart:
            item_quantity = request.POST.get(f'qty_{item}')
            checkout_items.append({
                'product': item,
                'quantity': item_quantity,
            })
        request.session['checkout'] = checkout_items
        return redirect('make_payment')

    context = {
        'products': products,
        'cart': cart,
        'prices': [p.selling_price for p in products],
    }
    return render(request, 'client_site/checkout.html', context)


def make_payment(request):
    checkout_items = request.session.get('checkout', [])
    order_items = []
    for item in checkout_items:
        product = Product.objects.get(pk=item['product'])
        order_items.append(Sale(
            product=product,
            quantity_sold=item['quantity'],
            total_cost=float(f"{item['quantity']}") * product.selling_price
        ))

    if request.method == 'POST':
        today = datetime.today()
        year = str(today.year)[-2:]
        month = str(today.month).zfill(2)
        day = str(today.day).zfill(2)
        order = Order(
            order_number=f'CP{_generate_random_string(3)}{year}{month}{day}',
            total_cost=sum([float(item.total_cost) for item in order_items]),
            client_name=request.POST.get('client_name'),
            client_email=request.POST.get('client_email'),
            proof_of_payment=request.FILES.get('proof_of_payment')
        )
        order.save()
        for item in order_items:
            item.order = order
            item.save()
        for item in checkout_items:
            product = Product.objects.get(pk=item['product'])
            product.quantity_in_stock -= int(f"{item['quantity']}")
            product.save()
        request.session['cart'] = []
        request.session['checkout'] = []

        # SEND MAIL
        html_message = render_to_string(
            'client_site/order_confirmation_mail_template.html', {
                'order': order,
            })

        subject = f'Your ColourPost Order is Confirmed - {order.order_number}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [order.client_email]
        send_mail(
            subject,
            '',
            from_email,
            recipient_list,
            html_message=html_message,
        )

        messages.success(
            request, 'Order has been recorded. You will receive an email containing the details of your order shortly.')
        return redirect('store')
    # request.session['cart'] = []
    # request.session['checkout'] = []
    return render(request, 'client_site/make_payment.html', {
        'checkout_items': checkout_items,
        'order_items': order_items,
    })
