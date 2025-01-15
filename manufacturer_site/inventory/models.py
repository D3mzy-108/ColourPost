from django.db import models


class RawMaterial(models.Model):
    units = [
        ('kgs', 'Kilograms'),
        ('lts', 'Liters'),
    ]
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    quantity_in_stock = models.IntegerField(default=0)
    measurement_unit = models.CharField(max_length=10, choices=units)
    cost_price = models.FloatField(default=0.0)

    class Meta:
        verbose_name = 'RawMaterial'
        verbose_name_plural = 'RawMaterials'

    def __str__(self):
        return f'{self.name} - {self.code}'
