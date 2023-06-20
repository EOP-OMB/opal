from django import forms
from .models import components


class ComponentForm(forms.ModelForm):
    scope = forms.CharField(max_length=100)
    policy_owner = forms.CharField(max_length=100)
    review_interval = forms.CharField(max_length=100)
    
    class Meta:
        model = components
        fields = ['type', 'title', 'purpose', 'status', 'scope','policy_owner','review_interval', 'description']
        



