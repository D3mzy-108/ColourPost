from django.urls import path
from .views import inventory, product_inventory, raw_materials, add_raw_materials, delete_raw_material

urlpatterns = [
    path('', inventory, name='inventory'),

    # PRODUCTS
    path('products/', product_inventory, name='product_inventory'),

    # RAW MATERIALS
    path('raw-materials/', raw_materials, name='raw_materials'),
    path('raw-materials/add/', add_raw_materials, name='add_raw_materials'),
    path('raw-materials/delete/',
         delete_raw_material, name='delete_raw_material'),
]
