from django.contrib import admin
from .models import RawMaterial, MaterialPurchaseLog


@admin.register(RawMaterial)
class RawMaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'alias', 'code', 'measurement_unit')
    search_fields = ('name', 'alias', 'code', 'measurement_unit')


@admin.register(MaterialPurchaseLog)
class MaterialPurchaseLogAdmin(admin.ModelAdmin):
    list_display = ('raw_material', 'quantity', 'ttl_cost', 'date')
    list_filter = ('date',)
    readonly_fields = ('raw_material', 'quantity', 'ttl_cost', 'date')
    search_fields = ('raw_material__name', 'raw_material__alias', 'date')
