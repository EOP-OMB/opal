from django import forms
from django.forms.widgets import SelectDateWidget
from ssp.models import system_characteristics
from datetime import datetime


class system_characteristics_form(forms.ModelForm):
    class Meta:
        model=system_characteristics
        fields = ('system_name', 'system_name_short', 'description', 'date_authorized', 'security_sensitivity_level', 'system_information', 'security_impact_level', 'security_objective_confidentiality', 'security_objective_integrity', 'security_objective_availability', 'status',)
        widgets = {'date_authorized': SelectDateWidget}
        initial = {'date_authorized': datetime.now()}







