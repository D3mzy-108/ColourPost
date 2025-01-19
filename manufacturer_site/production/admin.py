from django.contrib import admin
from .models import Production, ProductionResource, ProductionBatch, BatchItem


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


@admin.register(ProductionBatch)
class ProductionBatchAdmin(admin.ModelAdmin):
    list_display = ('production', 'volume_produced', 'ttl_cost', 'date')
    list_filter = ('date',)
    search_fields = ('production__production_code', 'date')


@admin.register(BatchItem)
class BatchItemAdmin(admin.ModelAdmin):
    search_fields = ('product', 'date')
