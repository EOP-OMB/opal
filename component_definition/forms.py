from django import forms
from catalog.models import controls, parts, catalogs
from component_definition.models import components, implementation_status_choices
from common.models import links, roles


class select_control_statements_form(forms.Form):
    catalog = forms.ModelChoiceField(queryset=catalogs.objects.all())
    controls = forms.ModelMultipleChoiceField(queryset=controls.objects.all())
    statements = forms.ModelMultipleChoiceField(queryset=parts.objects.all())


class component_statement_form(forms.Form):
    catalog = forms.ModelChoiceField(queryset=catalogs.objects.all())
    controls = forms.ModelChoiceField(queryset=controls.objects.none())
    statements = forms.ModelMultipleChoiceField(queryset=parts.objects.none())
    by_component = forms.ModelChoiceField(queryset=components.objects.all(), empty_label=None)
    description = forms.Textarea()
    # links = forms.ModelMultipleChoiceField(queryset=links.objects.all())
    status = forms.Select(choices=implementation_status_choices)
    responsible_roles = forms.ModelMultipleChoiceField(queryset=roles.objects.all())