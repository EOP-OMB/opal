from django.apps import apps
from django.contrib import admin
# from nested_inline.admin import NestedModelAdmin, NestedStackedInline

from common.admin import CustomAdmin
from component.models import by_components, components, control_implementations, implemented_requirements


# Not using this, implementation is strictly at the control level now. It was just much simpler
# class statementsTabularInline(NestedStackedInline):
#     model = statements
#     extra = 0
#     fk_name = 'implemented_requirement'
#     fields = ('statement_id',)
#     filter_horizontal = ('statement_id',)


# class by_componentTabularInline(NestedStackedInline):
#     model = by_components
#     extra = 1
#     fk_name = 'implemented_requirement'
#     fields = ('component_uuid', 'implementation_status', 'description', 'responsible_roles')
#     filter_horizontal = ('responsible_roles',)
#
#
# class implemented_requirementsTabularInline(NestedStackedInline):
#     model = implemented_requirements
#     extra = 1
#     fk_name = 'control_implementation'
#     inlines = [by_componentTabularInline]
#     fields = ('control_id',)
#
#
# class control_implementationsTabularInline(NestedStackedInline):
#     model = control_implementations
#     extra = 1
#     fk_name = 'component'
#     fields = ('description',)
#     inlines = [implemented_requirementsTabularInline]
#
#
# @admin.register(components)
# class componentsAdmin(NestedModelAdmin):
#     list_display = (
#         'title',
#         'type',
#         'status',
#         'created_at',
#         'updated_at',
#         )
#     list_filter = ('created_at', 'updated_at', 'status', 'type')
#     raw_id_fields = ('props', 'links', 'responsible_roles', 'protocols')
#     date_hierarchy = 'created_at'
#     inlines = [control_implementationsTabularInline]
#     fields = ('title', 'type', 'description', 'purpose', 'status')


# other models
models = apps.get_app_config('component').get_models()

for model in models:
    try:
        admin.site.register(model, CustomAdmin)
    except admin.sites.AlreadyRegistered:
        pass
