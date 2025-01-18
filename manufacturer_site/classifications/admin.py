from django.contrib import admin
from .models import Packaging, ProductType, Product


@admin.register(Packaging)
class PackagingAdmin(admin.ModelAdmin):
    list_display = ('alias', 'volume')
    search_fields = ('alias', 'volume')


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ('product_type', 'package')
    search_fields = ('product_color',)
