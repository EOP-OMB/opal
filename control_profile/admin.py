from django.apps import apps
from django.contrib import admin

from common.admin import CustomAdmin

# other models
models = apps.get_app_config('control_profile').get_models()

for model in models:
    try:
        admin.site.register(model, CustomAdmin)
    except admin.sites.AlreadyRegistered:
        pass
