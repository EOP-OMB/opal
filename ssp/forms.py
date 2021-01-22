from django import forms
from django.forms import ModelForm
from ssp.models import system_security_plan

class SystemSecurityPlan(ModelForm):
    class Meta:
        model = system_security_plan
        fields = '__all__'