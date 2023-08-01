from django.contrib import admin
from django.apps import apps
from common.admin import CustomAdmin
from .models import controls, available_catalog_list


@admin.register(controls)
class controls_admin(admin.ModelAdmin):
    list_filter = ('control_class',)


@admin.register(available_catalog_list)
class available_catalog_list_admin(admin.ModelAdmin):
    fields = ['name', 'link', 'catalog_uuid']
 

# other models
models = apps.get_app_config('catalog').get_models()

for model in models:
    try:
        admin.site.register(model, CustomAdmin)
    except admin.sites.AlreadyRegistered:
        pass
