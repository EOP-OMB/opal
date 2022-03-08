import logging

from django.contrib import admin
from django.apps import apps

# Register your models here.

def get_list_display(m, request):
    excluded_fields = ['created_at', 'updated_at']
    list_display = ()
    for field in m.opts.concrete_fields:
        print("field = " + field.name)
        if field.name not in excluded_fields:
            list_display + (field.name,)
            print(m.list_display)
    list_display + ('created_at',)
    list_display + ('updated_at',)
    return list_display


class CustomAdmin(admin.ModelAdmin):

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        """
        Get a form Field for a ManyToManyField. Tweak so filter_horizontal
        control used by default. If raw_id or autocomplete are specified
        will take precedence over this.
        """
        filter_horizontal_original = self.filter_horizontal
        self.filter_horizontal = (db_field.name,)
        form_field = super().formfield_for_manytomany(db_field, request=None, **kwargs)
        self.filter_horizontal = filter_horizontal_original
        return form_field


# other models
models = apps.get_app_config('common').get_models()

for model in models:
    try:
        admin.site.register(model, CustomAdmin)
    except admin.sites.AlreadyRegistered:
        pass