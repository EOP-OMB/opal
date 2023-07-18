from django.contrib.admin.widgets import AdminSplitDateTime
from django.shortcuts import reverse
from django.utils.safestring import mark_safe
from django.forms import widgets
from django import forms
from common.models import resources, base64, metadata, back_matter, props, links


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50, label="Document Title")
    file = forms.FileField(required=False)
    
        
class RelatedFieldWidgetCanAdd(widgets.SelectMultiple):

    def __init__(self, related_model, related_url=None, *args, **kw):
        super(RelatedFieldWidgetCanAdd, self).__init__(*args, **kw)

        if not related_url:
            rel_to = related_model
            info = (
            rel_to._meta.app_label,
            rel_to._meta.object_name.lower())
            related_url = 'admin:%s_%s_add' % info

        # Be careful that here "reverse" is not allowed
        self.related_url = related_url

    def render(self, name, value, *args, **kwargs):
        self.related_url = reverse(self.related_url)
        output = [super(RelatedFieldWidgetCanAdd, self).render(name, value, *args, **kwargs), '<a href="%s?_to_field=id&_popup=1" class="related-widget-wrapper-link add-related" id="add_id_%s" onclick="return showAddAnotherPopup(this);" target=_blank>' % (self.related_url, name), '<img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>']
        return mark_safe(''.join(output))


class resource_form(forms.ModelForm):
    class Meta:
        model = resources
        fields = "title", "description", "base64"
        widgets = {'base64': RelatedFieldWidgetCanAdd(base64, related_url='common:create_base64')}


class metadata_form(forms.ModelForm):
    class Meta:
        model=metadata
        fields = ('title','published','version')
        widgets = {'published': AdminSplitDateTime()}


class back_matter_form(forms.ModelForm):
    class Meta:
        model = back_matter
        fields = ('resources',)
        widgets = {'resources': RelatedFieldWidgetCanAdd(resources, related_url='common:add_resource_view')}


class links_form(forms.ModelForm):
    class Meta:
        model = links
        exclude = ["remarks"]


class props_form(forms.ModelForm):
    class Meta:
        model = props
        exclude = ["remarks"]