from django.db import models
from manufacturer_site.classifications.models import Product


class Order(models.Model):
    order_number = models.CharField(max_length=100)
    total_cost = models.FloatField(default=0.0)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    proof_of_payment = models.FileField(
        upload_to='proof-of-payment/', null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return self.order_number


class Sale(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT, related_name='sales')
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='product_sales')
    quantity_sold = models.IntegerField(default=0)
    total_cost = models.FloatField(default=0.0)

    class Meta:
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'

    def __str__(self):
        return f"{self.order.order_number} - {self.product}"
