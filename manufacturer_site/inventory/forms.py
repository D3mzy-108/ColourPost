from django import forms
from .models import RawMaterial, MaterialPurchaseLog
from manufacturer_site.classifications.models import Product


class RawMaterialForm(forms.ModelForm):
    measurement_unit = forms.ChoiceField(
        choices=RawMaterial.units, widget=forms.RadioSelect())

    class Meta:
        model = RawMaterial
        fields = ('name', 'alias', 'code', 'quantity_in_stock',
                  'measurement_unit', 'cost_price')


class MaterialPurchaseLogForm(forms.ModelForm):

    class Meta:
        model = MaterialPurchaseLog
        fields = ('raw_material', 'quantity', 'ttl_cost')


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('image',
        'product_color',
                  'quantity_in_stock',
                  'cost_price',
                  'selling_price',
                  'product_type',
                  'package',)
