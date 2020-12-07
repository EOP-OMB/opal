from django.contrib import admin
from django.apps import apps
from ssp import models


# Register your models here.

@admin.register(models.system_security_plan)
class systemSecurityPlanAdmin(admin.ModelAdmin):
    filter_horizontal = ['information_types','system_components', 'system_services', 'system_interconnections', 'system_inventory_items',
                         'controls', 'properties', 'links', 'leveraged_authorization', 'additional_selected_controls']
    fieldsets = (
        ('Title', {
            'fields': (('title', 'short_name'), 'desc')
        }),
        ('System', {
            'fields': (('published', 'lastModified','date_authorized','system_status'), ('version', 'oscalVersion'), 'control_baseline')
        }),
        ('FIPS Level', {
            'fields' : ('information_types',('security_objective_confidentiality','security_objective_integrity','security_objective_availability'))
        }),
        ('System Diagrams', {
            'fields' : (('authorization_boundary_diagram',
                         'network_architecture_diagram',
                         'data_flow_diagram'))
        }),
        ('Other', {
            'classes': ('collapse',),
            'fields': ('remarks','links','properties','annotations'),
        }),
    )

    def __str__(self):
        return "System Security Plans (SSPs)"


@admin.register(models.system_control)
class system_controlAdmin(admin.ModelAdmin):
    filter_horizontal = ['properties', 'annotations', 'links', 'control_parameters', 'control_statements']
    list_filter = ['control_origination', 'nist_control__group_title']
    list_display = ['title','short_name','nist_control']
    sortable_by = ['sort_id','nist_control']

    fieldsets = (
        ('Title', {
            'fields': (('title', 'short_name'), 'desc')
        }),
        ('System', {
            'fields': ('control_parameters', 'control_statements', 'control_status', 'control_origination','nist_control')
        }),
        ('Other', {
            'classes': ('collapse',),
            'fields': ('remarks', 'links', 'properties', 'annotations'),
        }),
    )

@admin.register(models.information_type)
class information_typeAdmin(admin.ModelAdmin):
    fields = ['title','short_name',('confidentialityImpact','integrityImpact','availabilityImpact'),'desc']
    list_display = ['short_name','title','confidentialityImpact','integrityImpact','availabilityImpact']
    sortable_by = ['short_name','title','confidentialityImpact','integrityImpact','availabilityImpact']

@admin.register(models.control_statement)
class control_statementAdmin(admin.ModelAdmin):
    filter_horizontal = ['control_statement_responsible_roles', 'properties', 'links', 'annotations']
    fields = ['title','short_name','control_statement_id','control_statement_responsible_roles','control_statement_text','links','desc']


@admin.register(models.control_parameter)
class control_parameterAdmin(admin.ModelAdmin):
    fields = [('title','short_name'),('control_parameter_id','value'),'desc']

@admin.register(models.control_baseline)
class control_baselineAdmin(admin.ModelAdmin):
    filter_horizontal = ['controls']


class nist_control_statementAdmin(admin.TabularInline):
    model = models.nist_control_statement
    extra = 0


@admin.register(models.nist_control)
class nist_controlAdmin(admin.ModelAdmin):
    filter_horizontal = ['parameters']
    list_filter = ['group_title']
    list_display = ['catalog', 'group_id', 'group_title', 'control_id', 'label']
    list_display_links = ['group_id', 'group_title', 'control_id', 'label']
    inlines = [nist_control_statementAdmin, ]


@admin.register(models.system_inventory_item)
class system_inventory_itemAdmin(admin.ModelAdmin):
    filter_horizontal = ['properties', 'links', 'annotations']
    list_filter = ['inventory_item_type']
    list_display = ['title', 'short_name', 'inventory_item_type', 'desc']


@admin.register(models.inventory_item_type)
class inventory_item_typeAdmin(admin.ModelAdmin):
    filter_horizontal = ['responsibleRoles', 'properties', 'links', 'annotations']
    list_display = ['title', 'use', 'desc', 'baseline_configuration']


@admin.register(models.system_interconnection)
class system_interconnectionAdmin(admin.ModelAdmin):
    filter_horizontal = ['interconnection_responsible_roles', 'properties', 'links', 'annotations']


@admin.register(models.link)
class linkAdmin(admin.ModelAdmin):
    list_display = ['text', 'href', 'mediaType', 'requires_authentication']
    list_editable = ['text', 'href', 'mediaType', 'requires_authentication']
    list_display_links = None


@admin.register(models.system_service)
class system_serviceAdmin(admin.ModelAdmin):
    list_display = ['title', 'desc']
    filter_horizontal = ['protocols', 'service_information_types', 'properties', 'annotations', 'links']
    list_filter = ['protocols']


@admin.register(models.system_component)
class system_componentAdmin(admin.ModelAdmin):
    filter_horizontal = ['component_information_types', 'component_responsible_roles', 'properties', 'annotations',
                         'links']
    list_filter = ['component_information_types', 'component_status', 'component_responsible_roles', 'component_type']
    list_display = ['component_title', 'component_type', 'component_description']


@admin.register(models.person)
class personAdmin(admin.ModelAdmin):
    filter_horizontal = ['organizations', 'locations', 'email_addresses', 'telephone_numbers', 'properties',
                         'annotations', 'links']
    list_display = ['name', ]
    list_filter = ['organizations', 'locations']


@admin.register(models.organization)
class organizationAdmin(admin.ModelAdmin):
    filter_horizontal = ['locations', 'email_addresses', 'telephone_numbers', 'properties', 'annotations', 'links']


# all other models
models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
