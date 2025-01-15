from django import forms
from .models import Packaging


class PackagingForm(forms.ModelForm):

    class Meta:
        model = Packaging
        fields = ('volume', 'alias')
