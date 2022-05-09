from django.contrib import admin
from django.apps import apps
from common.admin import CustomAdmin
from .models import controls

@admin.register(controls)
class controlsAdmin(admin.ModelAdmin):
    list_filter = ('control_class',)

# other models
models = apps.get_app_config('catalog').get_models()

for model in models:
    try:
        admin.site.register(model, CustomAdmin)
    except admin.sites.AlreadyRegistered:
        pass
