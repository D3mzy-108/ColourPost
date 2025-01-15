from django.urls import path
from .views import inventory, product_inventory, raw_materials

urlpatterns = [
    path('', inventory, name='inventory'),
    path('products/', product_inventory, name='product_inventory'),
    path('raw-materials/', raw_materials, name='raw_materials'),
]
