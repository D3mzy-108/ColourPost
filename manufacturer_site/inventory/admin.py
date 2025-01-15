from django.contrib import admin
from .models import RawMaterial


@admin.register(RawMaterial)
class RawMaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'alias', 'code', 'measurement_unit')
    search_fields = ('name', 'alias', 'code', 'measurement_unit')
