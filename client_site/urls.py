from django.urls import path
from .views import home, store, add_to_cart, remove_from_cart, checkout, make_payment

urlpatterns = [
    path('', home, name='home'),
    path('store/', store, name='store'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/',
         remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('checkout/payment/', make_payment, name='make_payment'),
]
