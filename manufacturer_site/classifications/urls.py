from django.urls import path
from .views import classifications, product_types, add_product_category, modify_product_category, delete_product_category, product_packaging, add_package, delete_package

urlpatterns = [
    path('', classifications, name='classifications'),

    # PRODUCT TYPES
    path('product-types/', product_types, name='product_types'),
    path('product-types/add/', add_product_category, name='add_product_category'),
    path('product-types/<int:id>/modify/', modify_product_category,
         name='modify_product_category'),
    path('product-types/delete/', delete_product_category,
         name='delete_product_category'),

    # PRODUCT PACKAGING
    path('product-packaging/', product_packaging, name='product_packaging'),
    path('product-packaging/add/', add_package, name='add_package'),
    path('product-packaging/delete/', delete_package, name='delete_package'),
]
