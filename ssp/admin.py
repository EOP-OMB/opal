from django.contrib import admin
from django.apps import apps
from django.utils.html import mark_safe
from ssp import models

# Register your models here.


# all other models
models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass