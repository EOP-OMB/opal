from django import forms
from catalog.models import controls, parts, catalogs
from component_definition.models import components, implementation_status_choices, by_components
from common.models import links, roles


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
    # by_component = forms.ModelChoiceField(queryset=components.objects.all(), empty_label=None)
    # description =
    # # links = forms.ModelMultipleChoiceField(queryset=links.objects.all())
    # status = forms.Select(choices=implementation_status_choices)
    # responsible_roles = forms.ModelMultipleChoiceField(queryset=roles.objects.all())
