from django import forms
from django.forms.widgets import SelectDateWidget, Select
from ssp.models import system_characteristics, import_profiles
from ctrl_profile.models import profiles
from datetime import datetime


class system_characteristics_form(forms.ModelForm):

    class Meta:
        model=system_characteristics
        fields = ('system_name', 'system_name_short', 'description', 'date_authorized', 'security_sensitivity_level', 'system_information', 'security_impact_level', 'security_objective_confidentiality', 'security_objective_integrity', 'security_objective_availability', 'status',)
        widgets = {'date_authorized': SelectDateWidget}
        initial = {'date_authorized': datetime.now()}


class import_profiles_form(forms.ModelForm):
    choices = []
    for profile in profiles.objects.all():
        choices.append((profile.get_permalink(),profile.__str__()))

    class Meta:
        model = import_profiles
        fields = ('href',)
        widgets = {'href': Select}







