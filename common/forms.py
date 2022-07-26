from django.shortcuts import reverse
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.conf import settings


class RelatedFieldWidgetCanAdd(widgets.Select):

    def __init__(self, related_model, related_url=None, *args, **kw):

        super(RelatedFieldWidgetCanAdd, self).__init__(*args, **kw)

        if not related_url:
            rel_to = related_model
            info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
            related_url = 'admin:%s_%s_add' % info

        # Be careful that here "reverse" is not allowed
        self.related_url = related_url

    def render(self, name, value, *args, **kwargs):
        self.related_url = reverse(self.related_url)
        output = [super(RelatedFieldWidgetCanAdd, self).render(name, value, *args, **kwargs),
                  '<a href="%s?_to_field=id&_popup=1" class="related-widget-wrapper-link add-related" id="add_id_%s" onclick="return showAddAnotherPopup(this);" target=_blank> ' % (self.related_url, name),
                  '<img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>']
        return mark_safe(''.join(output))
