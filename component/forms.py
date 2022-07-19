from django import forms

from catalog.models import catalogs, controls
from component.models import by_components, components
from common.models import roles


class select_control_statements_form(forms.Form):
    catalogs = forms.ModelChoiceField(queryset=catalogs.objects.all())
    controls = forms.ModelChoiceField(queryset=controls.objects.all())
    statements = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[]
        )


class component_statement_form(forms.Form):
    component_uuid = forms.ModelChoiceField(queryset=components.objects.all())
    implementation_status = forms.ChoiceField(choices=by_components.implementation_status.field.choices)
    responsible_roles = forms.ModelMultipleChoiceField(queryset=roles.objects.all())
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":60}))

# class component_statement_form(forms.ModelForm):
#     class Meta:
#         model = by_components
#         fields = ['component_uuid', 'description', 'implementation_status', 'responsible_roles']
