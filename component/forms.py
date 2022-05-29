from django import forms

from catalog.models import catalogs, controls
from component.models import by_components


class select_control_statements_form(forms.Form):
    catalog = forms.ModelChoiceField(queryset=catalogs.objects.all())
    controls = forms.ModelChoiceField(queryset=controls.objects.all())
    statements = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[],
    )


class component_statement_form(forms.ModelForm):
    class Meta:
        model = by_components
        fields = ['component_uuid', 'description', 'implementation_status', 'responsible_roles']
