# Generated by Django 4.2 on 2025-01-18 23:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classifications', '0005_product'),
        ('production', '0007_remove_productionbatch_is_up_to_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='BatchItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_produced', models.FloatField(default=0.0)),
                ('total_volume', models.FloatField(default=0.0)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batch_items', to='production.productionbatch')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='classifications.product')),
            ],
        ),
    ]
