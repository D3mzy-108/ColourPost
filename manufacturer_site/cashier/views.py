from django.shortcuts import render, get_object_or_404
from .models import Order
from django.db.models import Q


def sales(request):
    search_query = request.GET.get('q', '')
    orders = Order.objects.filter(
        Q(order_number__icontains=search_query) |
        Q(client_name__icontains=search_query) |
        Q(client_email__icontains=search_query)
    ).order_by('-date', '-id')
    context = {
        'orders': orders,
        'search_query': search_query,
    }
    return render(request, 'manufacturer_site/cashier/sales.html', context)


def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
    }
    return render(request, 'manufacturer_site/cashier/sales/order_details.html', context)
