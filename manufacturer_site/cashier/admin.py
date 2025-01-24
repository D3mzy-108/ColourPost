from django.contrib import admin
from .models import Order, Sale


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'client_name',
                    'client_email', 'total_cost', 'date')
    list_filter = ('date',)
    search_fields = ('order_number', 'client_name', 'client_email')


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity_sold', 'total_cost')
    search_fields = ('order__order_number',)
