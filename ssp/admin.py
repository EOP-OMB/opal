from django.contrib import admin
from django.apps import apps
from nested_inline.admin import NestedModelAdmin, NestedStackedInline

from common.admin import CustomAdmin, metadataAdminTabularInline

from ssp.models import system_security_plans


@admin.register(system_security_plans)
class system_security_plansAdmin(admin.ModelAdmin):
    list_display = (
        'metadata',
        'created_at',
        'updated_at',
        )
    list_filter = (
        'created_at',
        'updated_at',
        'metadata',
        'import_profile',
        'system_characteristics',
        'system_implementation',
        'control_implementation',
        'back_matter',
    )
    date_hierarchy = 'updated_at'
    # inlines = [ssp_metadata_Inline]


# other models
models = apps.get_app_config('ssp').get_models()

for model in models:
    try:
        admin.site.register(model, CustomAdmin)
    except admin.sites.AlreadyRegistered:
        pass
