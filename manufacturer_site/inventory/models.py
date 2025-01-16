from django.db import models


class RawMaterial(models.Model):
    units = [
        ('kgs', 'Kilograms'),
        ('lts', 'Liters'),
    ]
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    quantity_in_stock = models.FloatField(default=0.0)
    measurement_unit = models.CharField(max_length=10, choices=units)
    cost_price = models.FloatField(default=0.0)

    class Meta:
        verbose_name = 'RawMaterial'
        verbose_name_plural = 'RawMaterials'

    def __str__(self):
        return f'{self.name} - {self.code}'


class MaterialPurchaseLog(models.Model):
    raw_material = models.ForeignKey(
        RawMaterial, on_delete=models.CASCADE, related_name='purchase_logs')
    quantity = models.FloatField(default=0.0)
    ttl_cost = models.FloatField(default=0.0)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'MaterialPurchaseLog'
        verbose_name_plural = 'MaterialPurchaseLogs'

    def save(self, *args):
        self.raw_material.quantity_in_stock += self.quantity
        self.raw_material.cost_price = self.ttl_cost / self.quantity
        self.raw_material.save()
        return super().save()

    def __str__(self):
        return f'{self.raw_material} ~ {self.date}'
