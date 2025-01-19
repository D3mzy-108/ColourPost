from django import forms
from .models import Packaging, ProductType
from manufacturer_site.inventory.models import RawMaterial


class PackagingForm(forms.ModelForm):

    class Meta:
        model = Packaging
        fields = ('volume', 'alias')


class ProductTypeForm(forms.ModelForm):
    raw_materials = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = ProductType
        fields = ('name', 'raw_materials')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate raw_material_choices
        raw_material_choices = [
            (f'{material.id}', material) for material in RawMaterial.objects.all()
        ]
        self.fields['raw_materials'].choices = raw_material_choices
