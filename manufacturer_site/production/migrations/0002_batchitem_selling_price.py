# Generated by Django 4.2 on 2025-01-20 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='batchitem',
            name='selling_price',
            field=models.FloatField(default=0.0),
        ),
    ]
