from django.urls import path
from .views import classifications, product_types, product_packaging, add_package, delete_package

urlpatterns = [
    path('', classifications, name='classifications'),
    path('product-types/', product_types, name='product_types'),

    # PRODUCT PACKAGING
    path('product-packaging/', product_packaging, name='product_packaging'),
    path('product-packaging/add/', add_package, name='add_package'),
    path('product-packaging/delete/', delete_package, name='delete_package'),
]
