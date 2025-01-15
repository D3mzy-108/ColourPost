from django.db import models


class Packaging(models.Model):
    volume = models.IntegerField(default=0)
    alias = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Packaging'
        verbose_name_plural = 'Packages'

    def __str__(self):
        pass
