from django import forms

from common.forms import RelatedFieldWidgetCanAdd
from common.models import props, links
from .models import components


class ComponentForm(forms.ModelForm):
    
    class Meta:
        model = components
        # fields = ['type', 'title', 'purpose', 'status', 'props', 'description', 'links']
        fields = ['type', 'title', 'purpose', 'status', 'description']
        # widgets = {'props': RelatedFieldWidgetCanAdd(props, related_url='common:add_props_view'),'links': RelatedFieldWidgetCanAdd(links, related_url='common:add_links_view')                   }
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(style="width: inherit;")
        self.fields['purpose'].widget.attrs.update(style="width: inherit;")
        self.fields['status'].widget.attrs.update(style="width: inherit;")
        self.fields['type'].widget.attrs.update(style="width: inherit;")
        self.fields['description'].label = ("Description")
        # self.fields['props'].widget.attrs.update(style="width: inherit;")
        # self.fields['links'].widget.attrs.update(style="width: inherit;")

