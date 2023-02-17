from django.apps import apps
from django.contrib import admin

from common.admin import CustomAdmin
from component.models import components, control_implementations


@admin.register(control_implementations)
class control_implementations_admin(CustomAdmin):
    model = control_implementations


class control_implementations_inline(admin.StackedInline):
    model = control_implementations
    extra = 0
    fields = ['description', 'implemented_requirements']
    filter_horizontal = ['implemented_requirements']


@admin.register(components)
class componentsAdmin(CustomAdmin):
    def get_list_display(self, request):
        return ['title', 'type', 'status', 'created_at', 'updated_at']

    list_filter = ('created_at', 'updated_at', 'status', 'type')
    # raw_id_fields = ('props', 'links', 'responsible_roles', 'protocols')
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {'fields': ('title', 'type', 'description', 'purpose', 'status')}),
        ('Other Fields', {
            'classes': ('collapse',),
            'fields': ('props', 'links', 'responsible_roles', 'protocols')}),
    )
    inlines = [control_implementations_inline]


# other models
models = apps.get_app_config('component').get_models()

for model in models:
    try:
        admin.site.register(model, CustomAdmin)
    except admin.sites.AlreadyRegistered:
        pass
