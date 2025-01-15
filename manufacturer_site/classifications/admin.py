from django.contrib import admin
from .models import Packaging


@admin.register(Packaging)
class PackagingAdmin(admin.ModelAdmin):
    list_display = ('alias', 'volume')
    search_fields = ('alias', 'volume')
