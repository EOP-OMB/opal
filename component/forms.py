from django import forms
from .models import components


class ComponentForm(forms.ModelForm):
    class Meta:
        model = components
        fields = ['type', 'title', 'purpose', 'status', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(style="width: inherit;")
        self.fields['purpose'].widget.attrs.update(style="width: inherit;")
        self.fields['status'].widget.attrs.update(style="width: inherit;")
        self.fields['type'].widget.attrs.update(style="width: inherit;")

