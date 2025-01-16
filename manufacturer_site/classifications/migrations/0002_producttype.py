# Generated by Django 4.2 on 2025-01-16 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_rawmaterial_quantity_in_stock_and_more'),
        ('classifications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('raw_materials', models.ManyToManyField(related_name='materials', to='inventory.rawmaterial')),
            ],
            options={
                'verbose_name': 'ProductType',
                'verbose_name_plural': 'ProductTypes',
            },
        ),
    ]
