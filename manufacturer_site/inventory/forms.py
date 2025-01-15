from django import forms
from .models import RawMaterial, MaterialPurchaseLog


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
