from django.urls import path
from .views import classifications, product_types, product_packaging

urlpatterns = [
    path('', classifications, name='classifications'),
    path('product-types/', product_types, name='product_types'),
    path('product-packaging/', product_packaging, name='product_packaging'),
]
