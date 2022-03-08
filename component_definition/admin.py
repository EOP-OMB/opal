from django.contrib import admin

# Register your models here.

from .models import responsible_roles, parameters, control_implementations, components, implemented_requirements, statements, by_components, export, inherited, satisfied, responsibilities, provided_control_implementation
from .admin_inline_fields import *

@admin.register(responsible_roles)
class responsible_rolesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'role_id',
    )
    list_filter = ('created_at', 'updated_at', 'role_id')
    raw_id_fields = ('props', 'links', 'party_uuids')
    date_hierarchy = 'created_at'


@admin.register(parameters)
class parametersAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'param_id',
        'values',
    )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(control_implementations)
class control_implementationsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'description',
    )
    list_filter = ('created_at', 'updated_at')
    raw_id_fields = ('set_parameters',)
    date_hierarchy = 'created_at'
    inlines = (implemented_requirements_inline,)


@admin.register(components)
class componentsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'type',
        'title',
        'description',
        'purpose',
        'status',
    )
    list_filter = ('created_at', 'updated_at')
    raw_id_fields = (
        'props',
        'links',
        'responsible_roles',
        'protocols',
        'control_implementations',
    )
    inlines = (responsible_roles_inline,protocols_inline,control_implementations_inline)
    date_hierarchy = 'created_at'


@admin.register(implemented_requirements)
class implemented_requirementsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'control_id',
    )
    list_filter = ('created_at', 'updated_at', 'control_id')
    raw_id_fields = (
        'props',
        'links',
        'set_parameters',
        'responsible_roles',
        'statements',
        'by_components',
    )
    date_hierarchy = 'created_at'


@admin.register(statements)
class statementsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'statement_id',
    )
    list_filter = ('created_at', 'updated_at')
    raw_id_fields = ('props', 'links', 'responsible_roles', 'by_components')
    date_hierarchy = 'created_at'


@admin.register(by_components)
class by_componentsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'description',
        'implementation_status',
        'export',
    )
    list_filter = ('created_at', 'updated_at', 'export')
    raw_id_fields = (
        'component_uuid',
        'props',
        'links',
        'set_parameters',
        'inherited',
        'satisfied',
        'responsible_roles',
    )
    date_hierarchy = 'created_at'


@admin.register(export)
class exportAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'description',
    )
    list_filter = ('created_at', 'updated_at')
    raw_id_fields = ('props', 'links', 'provided', 'responsibilities')
    date_hierarchy = 'created_at'


@admin.register(inherited)
class inheritedAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'provided_uuid',
        'description',
    )
    list_filter = ('created_at', 'updated_at', 'provided_uuid')
    raw_id_fields = ('props', 'links', 'responsible_roles')
    date_hierarchy = 'created_at'


@admin.register(satisfied)
class satisfiedAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'responsibility_uuid',
        'description',
    )
    list_filter = ('created_at', 'updated_at', 'responsibility_uuid')
    raw_id_fields = ('props', 'links', 'responsible_roles')
    date_hierarchy = 'created_at'


@admin.register(responsibilities)
class responsibilitiesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'provided_uuid',
        'description',
    )
    list_filter = ('created_at', 'updated_at', 'provided_uuid')
    raw_id_fields = ('props', 'links', 'responsible_roles')
    date_hierarchy = 'created_at'


@admin.register(provided_control_implementation)
class provided_control_implementationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'description',
    )
    list_filter = ('created_at', 'updated_at')
    raw_id_fields = ('props', 'links', 'responsible_roles')
    date_hierarchy = 'created_at'


