# Generated by Django 4.2 on 2025-01-17 20:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0003_productionresource'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productionresource',
            old_name='materials',
            new_name='material',
        ),
    ]
