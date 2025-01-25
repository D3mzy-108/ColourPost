from django.urls import path
from .views import sales, order_details

urlpatterns = [
    path('sales/', sales, name='sales'),
    path('order/<int:order_id>/details/', order_details, name='order_details'),
]
