from django.contrib import admin
from .models import Packaging, ProductType


@admin.register(Packaging)
class PackagingAdmin(admin.ModelAdmin):
    list_display = ('alias', 'volume')
    search_fields = ('alias', 'volume')


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    '''Admin View for ProductType'''

    list_display = ('name',)
    search_fields = ('name',)
