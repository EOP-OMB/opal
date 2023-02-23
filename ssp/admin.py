from django.contrib import admin
from django.apps import apps
from common.admin import CustomAdmin
from ssp.models import system_security_plans, system_characteristics

@admin.register(system_characteristics)
class system_characteristicsAdmin(CustomAdmin):
    list_filter = (
        'created_at',
        'updated_at',)
    fieldsets = (
        ('System Name', {'fields':[('system_name','system_name_short')]}),
        ('Description', {'fields': [('description')]}),
        ('Authorization:', {'fields': ['status','date_authorized']}),
        ('Security Impact Level', {'fields': ['security_impact_level','security_objective_confidentiality','security_objective_integrity','security_objective_availability']}),
        ('Diagrams', {'fields': ['authorization_boundary','network_architecture','data_flow']}),
        ('Advanced', {'fields': ['system_ids','props','links','responsible_parties'],'classes': ('collapse',),})
    )


# class system_characteristics_inline(admin.StackedInline):
#     model = system_characteristics
#     extra = 0
#     fieldsets = (
#         ('System Name', {'fields':[('system_name','system_name_short')]}),
#         ('Description', {'fields': [('description')]}),
#         ('Authorization:', {'fields': ['status','date_authorized']}),
#         ('Security Impact Level', {'fields': ['security_impact_level','security_objective_confidentiality','security_objective_integrity','security_objective_availability']}),
#         ('Diagrams', {'fields': ['authorization_boundary','network_architecture','data_flow']}),
#     )

class system_implementationsAdmin(CustomAdmin):
    fields = ('remarks','leveraged_authorizations','components','inventory_items','users')




@admin.register(system_security_plans)
class system_security_plansAdmin(CustomAdmin):
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
    fields = ['metadata','system_characteristics','import_profile','system_implementation','back_matter']



# other models
models = apps.get_app_config('ssp').get_models()

for model in models:
    try:
        admin.site.register(model, CustomAdmin)
    except admin.sites.AlreadyRegistered:
        pass
