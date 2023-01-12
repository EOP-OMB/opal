from django import forms
from ssp.models import system_security_plans, system_characteristics, system_implementations, control_implementations
from common.models import metadata, back_matter
from common.forms import RelatedFieldWidgetCanAdd


class sspForm(forms.ModelForm):
    metadata = forms.ModelChoiceField(required=True, queryset=metadata.objects.all(), widget=RelatedFieldWidgetCanAdd(metadata, related_url='admin:common_metadata_add'))
    system_characteristics = forms.ModelChoiceField(required=True, queryset=system_characteristics.objects.all(), widget=RelatedFieldWidgetCanAdd(system_characteristics, related_url='admin:ssp_system_characteristics_add'))
    system_implementation = forms.ModelChoiceField(required=True, queryset=system_implementations.objects.all(), widget=RelatedFieldWidgetCanAdd(metadata, related_url='admin:ssp_system_implementations_add'))
    control_implementation = forms.ModelChoiceField(required=True, queryset=control_implementations.objects.all(), widget=RelatedFieldWidgetCanAdd(metadata, related_url='admin:component_control_implementations_add'))

    class Meta:
        model = system_security_plans
        fields = 'metadata', 'system_characteristics', 'system_implementation', 'control_implementation'


class