from django.contrib import admin
from django.apps import apps
from django.db import models


class BaseAdmin(admin.ModelAdmin):
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

# Register your models here.


# all other models
models = apps.get_models()

for model in models:
    try:
        admin.site.register(model,BaseAdmin)
    except admin.sites.AlreadyRegistered:
        pass