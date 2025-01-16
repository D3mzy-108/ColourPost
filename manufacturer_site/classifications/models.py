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
