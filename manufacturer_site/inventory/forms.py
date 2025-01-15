from django import forms
from .models import RawMaterial


class RawMaterialForm(forms.ModelForm):
    measurement_unit = forms.ChoiceField(
        choices=RawMaterial.units, widget=forms.RadioSelect())

    class Meta:
        model = RawMaterial
        fields = ('name', 'alias', 'code', 'quantity_in_stock',
                  'measurement_unit', 'cost_price')
