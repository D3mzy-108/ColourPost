from django.urls import path
from .views import inventory, product_inventory, new_product, product_details, raw_materials, add_raw_materials, delete_raw_material, material_purchase_log, create_purchase_log

urlpatterns = [
    path('', inventory, name='inventory'),

    # PRODUCTS
    path('products/', product_inventory, name='product_inventory'),
    path('products/new/', new_product, name='new_product'),
    path('products/<int:id>/details/', product_details, name='product_details'),

    # RAW MATERIALS
    path('raw-materials/', raw_materials, name='raw_materials'),
    path('raw-materials/add/', add_raw_materials, name='add_raw_materials'),
    path('raw-materials/delete/',
         delete_raw_material, name='delete_raw_material'),
    path('raw-materials/purchase-log/',
         material_purchase_log, name='material_purchase_log'),
    path('raw-materials/purchase-log/create/',
         create_purchase_log, name='create_purchase_log'),
]
