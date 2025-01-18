from django.db import models
from manufacturer_site.inventory.models import RawMaterial


class Packaging(models.Model):
    volume = models.IntegerField(default=0)
    alias = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Packaging'
        verbose_name_plural = 'Packages'

    def __str__(self):
        return self.alias


class ProductType(models.Model):
    name = models.CharField(max_length=100)
    raw_materials = models.ManyToManyField(
        RawMaterial, related_name='materials')

    class Meta:
        verbose_name = 'ProductType'
        verbose_name_plural = 'ProductTypes'

    def __str__(self):
        return self.name


class Product(models.Model):
    product_color = models.CharField(max_length=100)
    quantity_in_stock = models.IntegerField(default=0)
    cost_price = models.FloatField(default=0.0)
    selling_price = models.FloatField(default=0.0)
    product_type = models.ForeignKey(
        ProductType, on_delete=models.PROTECT, related_name='products')
    package = models.ForeignKey(
        Packaging, on_delete=models.PROTECT, related_name='products')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f'{self.product_color} {self.product_type.name} {self.package.alias}'
