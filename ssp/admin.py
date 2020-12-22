from django.contrib import admin
from django.apps import apps
from ssp import models


# Register your models here.

@admin.register(models.system_security_plan)
class systemSecurityPlanAdmin(admin.ModelAdmin):
    filter_horizontal = ['information_types', 'system_components', 'system_services', 'system_interconnections',
                         'system_inventory_items',
                         'controls', 'properties', 'links', 'leveraged_authorization', 'additional_selected_controls']
    fieldsets = (
        ('Title', {
            'fields': (('title', 'short_name'), 'desc')
        }),
        ('System', {
            'fields': (('published', 'lastModified', 'date_authorized', 'system_status'), ('version', 'oscalVersion'),
                       'control_baseline')
        }),
        ('FIPS Level', {
            'fields': ('information_types', (
                'security_objective_confidentiality', 'security_objective_integrity',
                'security_objective_availability'))
        }),
        ('Users', {
            'fields': ['system_users',]
        }),
        ('System Diagrams', {
            'fields': (('authorization_boundary_diagram',
                        'network_architecture_diagram',
                        'data_flow_diagram'))
        }),
        ('Other', {
            'classes': ('collapse',),
            'fields': ('remarks', 'links', 'properties', 'annotations'),
        }),
    )

    def __str__(self):
        return "System Security Plans (SSPs)"


@admin.register(models.system_control)
class system_controlAdmin(admin.ModelAdmin):
    filter_horizontal = ['properties', 'annotations', 'links', 'control_parameters', 'control_statements']
    list_filter = ['control_origination', 'nist_control__group_title']
    list_display = ['title', 'short_name', 'nist_control']
    sortable_by = ['sort_id', 'nist_control']

    fieldsets = (
        ('Title', {
            'fields': (('title', 'short_name'), 'desc')
        }),
        ('System', {
            'fields': (
                'control_parameters', 'control_statements', 'control_status', 'control_origination', 'nist_control')
        }),
        ('Other', {
            'classes': ('collapse',),
            'fields': ('remarks', 'links', 'properties', 'annotations'),
        }),
    )


@admin.register(models.information_type)
class information_typeAdmin(admin.ModelAdmin):
    fields = ['title', 'short_name', ('confidentialityImpact', 'integrityImpact', 'availabilityImpact'), 'desc']
    list_display = ['short_name', 'title', 'confidentialityImpact', 'integrityImpact', 'availabilityImpact']
    sortable_by = ['short_name', 'title', 'confidentialityImpact', 'integrityImpact', 'availabilityImpact']


@admin.register(models.control_statement)
class control_statementAdmin(admin.ModelAdmin):
    filter_horizontal = ['control_statement_responsible_roles', 'properties', 'links', 'annotations']
    fields = ['title', 'short_name', 'control_statement_id', 'control_statement_responsible_roles',
              'control_statement_text', 'links', 'desc']


@admin.register(models.control_parameter)
class control_parameterAdmin(admin.ModelAdmin):
    fields = [('title', 'short_name'), ('control_parameter_id', 'value'), 'desc']


@admin.register(models.control_baseline)
class control_baselineAdmin(admin.ModelAdmin):
    filter_horizontal = ['controls']


class nist_control_parameterAdmin(admin.TabularInline):
    model = models.nist_control_parameter
    extra = 0

class nist_control_statementAdmin(admin.TabularInline):
    model = models.nist_control_statement
    extra = 0

@admin.register(models.nist_control)
class nist_controlAdmin(admin.ModelAdmin):
    list_filter = ['catalog','group_title']
    list_display = ['catalog', 'group_title', 'control_id', 'label']
    list_display_links = ['catalog', 'group_title', 'control_id', 'label']
    ordering = ('sort_id','catalog')
    inlines = [nist_control_parameterAdmin,nist_control_statementAdmin,]


@admin.register(models.link)
class linkAdmin(admin.ModelAdmin):
    list_display = ['text', 'href', 'mediaType', 'requires_authentication']
    list_editable = ['text', 'href', 'mediaType', 'requires_authentication']
    list_display_links = None


# TODO I'd like these to be inline for person...
# class emailAdmin(admin.TabularInline):
#     model = models.email
#     extra = 1
#
# class phoneAdmin(admin.TabularInline):
#     model = models.telephone_number
#     extra = 1
#
# class locationAdmin(admin.TabularInline):
#     model = models.location
#     extra = 1

@admin.register(models.person)
class personAdmin(admin.ModelAdmin):
    filter_horizontal = ['organizations', 'locations', 'properties',
                         'annotations', 'links']
    list_display = ['name', ]
    list_filter = ['organizations', 'locations']
    # inlines = [emailAdmin,phoneAdmin,locationAdmin]

    fieldsets = (
        ('Title', {
            'fields': ('title', 'short_name',)
        }),
        ('Description', {
            'classes': ('collapse',),
            'fields': ['desc',]
        }),
        ('ID', {
            'fields': (
                'name',)
        }),
        ('Contact', {
            'fields': (
                'email_addresses', 'telephone_numbers', 'locations',)
        }),
        ('Groups', {
            'fields': ['organizations',]
        }),
    )


# all other models
models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
