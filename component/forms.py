from django import forms
from .models import components


class components_form(forms.ModelForm):
    class Meta:
        model = components
        exclude = ['remarks', 'props', 'protocols']
