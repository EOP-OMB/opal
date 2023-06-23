from django.apps import apps
from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from nested_admin.nested import NestedStackedInline

from common.admin import CustomAdmin
from component.models import components, control_implementations, parameters, implemented_requirements


@admin.register(parameters)
class parameters_admin(CustomAdmin):
    list_display = (
    'param_id',
    'values',
    'by_component',
    'created_at',
    'updated_at',
    )
    list_filter = ('created_at', 'updated_at', 'param_id', 'by_component')
    date_hierarchy = 'updated_at'
    fieldsets = (
        (None, {'fields': ('param_id','values',)}),
        ('Component', {'fields': ('by_component',)}),
    )


class parameters_inline(NestedStackedInline):
    model = parameters
    extra = 0
    fields = ['param_id','values']


class control_implementations_inline(NestedStackedInline):
    model = control_implementations
    extra = 0
    fields = ['implemented_requirements']
    filter_horizontal = ['implemented_requirements']
    inlines = [parameters_inline]

@admin.register(components)
class components_admin(CustomAdmin):
    def get_list_display(self, request):
        return ['title', 'type', 'status', 'created_at', 'updated_at']

    list_filter = ('created_at', 'updated_at', 'status', 'type')
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {'fields': ('title', 'type', 'props', 'description', 'purpose', 'status')}),
        ('Other Fields', {
            'classes': ('collapse',),
            'fields': ('links', 'responsible_roles', 'protocols')}),
    )
    inlines = [control_implementations_inline]


# other models
models = apps.get_app_config('component').get_models()

for model in models:
    try:
        admin.site.register(model, CustomAdmin)
    except admin.sites.AlreadyRegistered:
        pass
