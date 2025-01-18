from django.contrib import admin
from .models import Production, ProductionResource


@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = ('production_code', 'product_type', 'date', 'is_completed')
    list_filter = ('date', 'is_completed')
    search_fields = ('production_code', 'product_type__alias',
                     'date', 'is_completed')


@admin.register(ProductionResource)
class ProductionResourceAdmin(admin.ModelAdmin):
    list_display = ('production',
                    'material', 'quantity_used', 'ttl_cost')
    search_fields = ('production__production_code',
                     'material__name')
    list_filter = ('production__date', 'production__is_completed')
