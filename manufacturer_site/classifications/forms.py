from django import forms
from .models import Packaging, ProductType
from manufacturer_site.inventory.models import RawMaterial


class PackagingForm(forms.ModelForm):

    class Meta:
        model = Packaging
        fields = ('volume', 'alias')


class ProductTypeForm(forms.ModelForm):
    raw_material_choices = [
        (f'{material.id}', material) for material in RawMaterial.objects.all()
    ]
    raw_materials = forms.MultipleChoiceField(
        choices=raw_material_choices,
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = ProductType
        fields = ('name', 'raw_materials')
