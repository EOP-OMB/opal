from django import forms

from common.forms import RelatedFieldWidgetCanAdd
from common.models import props, links
from .models import components


class ComponentForm(forms.ModelForm):
    # scope = forms.CharField(max_length=100)
    # policy_owner = forms.CharField(max_length=100)
    # review_interval = forms.CharField(max_length=100)
    
    class Meta:
        model = components
        fields = ['type', 'title', 'purpose', 'status', 'props', 'description', 'links']
        widgets = {'props': RelatedFieldWidgetCanAdd(props, related_url='common:add_props_view'),
                   'links': RelatedFieldWidgetCanAdd(links, related_url='common:add_links_view')
                   }
        



