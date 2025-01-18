from django.db import models
from manufacturer_site.classifications.models import ProductType
from manufacturer_site.inventory.models import RawMaterial


class Production(models.Model):
    production_code = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    product_type = models.ForeignKey(
        ProductType, on_delete=models.PROTECT, related_name='productions', null=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Production'
        verbose_name_plural = 'Productions'

    def __str__(self):
        return self.production_code


class ProductionResource(models.Model):
    production = models.ForeignKey(
        Production, on_delete=models.CASCADE, related_name='resources')
    material = models.ForeignKey(RawMaterial, on_delete=models.PROTECT)
    quantity_used = models.FloatField(default=0.0)
    ttl_cost = models.FloatField(default=0.0)

    class Meta:
        verbose_name = 'ProductionResource'
        verbose_name_plural = 'ProductionResources'

    def save(self, *args):
        # CALCULATE COST
        material_cost = self.material.cost_price
        ttl_cost = (material_cost * self.quantity_used)
        self.ttl_cost = ttl_cost

        # CALCULATE BATCH COST
        batch = ProductionBatch.objects.get(production=self.production)
        production_cost = 0
        for resource in ProductionResource.objects.filter(production__id=self.production.id):
            if self.pk == resource.pk:
                production_cost += self.ttl_cost
            else:
                production_cost += resource.ttl_cost
        batch.ttl_cost = production_cost
        batch.save()

        return super().save()

    def delete(self, *args):
        batch = ProductionBatch.objects.get(production=self.production)
        batch.ttl_cost -= self.ttl_cost
        batch.save()
        return super().delete()

    def __str__(self):
        return self.production.production_code


class ProductionBatch(models.Model):
    production = models.OneToOneField(
        Production, on_delete=models.CASCADE, related_name='batch')
    volume_produced = models.FloatField(default=0.0)
    ttl_cost = models.FloatField(default=0.0)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'ProductionBatch'
        verbose_name_plural = 'ProductionBatches'

    def __str__(self):
        return self.production.production_code
