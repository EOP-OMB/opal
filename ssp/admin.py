from django.contrib import admin
from django.apps import apps
from django.utils.html import mark_safe
from ssp import models


# Register your models here.

@admin.register(models.system_security_plan)
class systemSecurityPlanAdmin(admin.ModelAdmin):
    filter_horizontal = ['information_types', 'system_services', 'system_interconnections',
                         'system_inventory_items', 'properties', 'links', 'leveraged_authorization',
                         'additional_selected_controls']
    filter_vertical = ['controls', 'system_components']

    fieldsets = (
        ('Title', {
            'fields': (('title', 'short_name'), 'desc')
        }),
        ('System', {
            'fields': (('published', 'date_authorized', 'system_status', 'authorization_revocation_date', 'authorization_revocation_reason'), ('version', 'oscalVersion'),
                       'control_baseline', 'controls', 'system_components', 'system_services', 'system_interconnections','system_inventory_items')
        }),
        ('FIPS Level', {
            'fields': ('information_types', (
                'security_objective_confidentiality', 'security_objective_integrity',
                'security_objective_availability'))
        }),
        ('Users', {
            'fields': ['system_users', ]
        }),
        ('System Diagrams', {
            'fields': (('authorization_boundary_diagram',
                        'network_architecture_diagram',
                        'data_flow_diagram'))
        }),
        ('Other', {
            'classes': ('collapse',),
            'fields': ('remarks', 'links', 'properties', 'annotations', 'organizational_unit', 'system_operator_type', 'public'),
        }),
    )

    def __str__(self):
        return "System Security Plans (SSPs)"


@admin.register(models.control_statement)
class control_statementAdmin(admin.ModelAdmin):
    filter_horizontal = ['control_statement_responsible_roles', 'properties', 'links', 'annotations']
    # fields = ['title', 'short_name', 'control_statement_id', 'control_statement_responsible_roles','control_statement_text', 'links', 'desc']
    readonly_fields = ['nist_control_text', ]

    fieldsets = (
        ('NIST', {
            'fields': ('nist_control_text',)
        }),
        ('Title', {
            'fields': ('title', 'short_name')
        }),
        ('Statement', {
            'fields': (
                ('control_statement_id', 'control_statement_text'), 'control_statement_responsible_roles', 'links',
                'remarks')
        }),
        ('Other', {
            'classes': ('collapse',),
            'fields': ('properties', 'annotations', 'desc'),
        }),
    )


@admin.register(models.control_parameter)
class control_parameterAdmin(admin.ModelAdmin):
    fields = [('title', 'short_name'), ('control_parameter_id', 'value'), 'desc']


class control_parameterInline(admin.TabularInline):
    model = models.system_control.control_parameters.through
    readonly_fields = ['parameter']
    ordering = ['control_parameter_id']
    extra = 0

    def parameter(self, instance):
        return mark_safe(instance.control_parameter.value)

    parameter.short_description = 'parameter value'


class control_statementInline(admin.TabularInline):
    model = models.system_control.control_statements.through
    readonly_fields = ['statement']
    ordering = ['control_statement_id']
    extra = 0

    def statement(self, instance):
        return mark_safe(instance.control_statement.control_statement_text)

    statement.short_description = 'Statement'


@admin.register(models.system_control)
class system_controlAdmin(admin.ModelAdmin):
    filter_horizontal = ['properties', 'annotations', 'links', 'control_parameters', 'control_statements']
    list_filter = ['control_primary_system','control_origination', 'nist_control__group_title']
    list_display = ['title', 'short_name', 'nist_control']
    sortable_by = ['sort_id', 'nist_control']
    inlines = [control_parameterInline, control_statementInline]
    readonly_fields = ['nist_control_text', ]

    fieldsets = (
        ('NIST', {
            'fields': ('nist_control_text',)
        }),
        ('Title', {
            'fields': ('title', 'short_name')
        }),
        ('System', {
            'fields': (
                'control_status', 'control_origination', 'nist_control', 'control_primary_system')
        }),
        ('Other', {
            'classes': ('collapse',),
            'fields': ('remarks', 'links', 'properties', 'annotations', 'desc'),
        }),
    )


@admin.register(models.information_type)
class information_typeAdmin(admin.ModelAdmin):
    fields = ['title', 'short_name', ('confidentialityImpact', 'integrityImpact', 'availabilityImpact'), 'desc']
    list_display = ['short_name', 'title', 'confidentialityImpact', 'integrityImpact', 'availabilityImpact']
    sortable_by = ['short_name', 'title', 'confidentialityImpact', 'integrityImpact', 'availabilityImpact']


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
    list_filter = ['catalog', 'group_title']
    list_display = ['catalog', 'group_title', 'control_id', 'label']
    list_display_links = ['catalog', 'group_title', 'control_id', 'label']
    ordering = ('sort_id', 'catalog')
    inlines = [nist_control_parameterAdmin, nist_control_statementAdmin, ]


@admin.register(models.link)
class linkAdmin(admin.ModelAdmin):
    list_display = ['text', 'href', 'rel', 'mediaType', 'requires_authentication']
    list_editable = ['text', 'href', 'rel', 'mediaType', 'requires_authentication']
    list_display_links = None


class emailInline(admin.TabularInline):
    model = models.person.email_addresses.through
    extra = 1


class phoneInline(admin.TabularInline):
    model = models.person.telephone_numbers.through
    extra = 1


class locationInline(admin.TabularInline):
    model = models.person.locations.through
    extra = 1


@admin.register(models.person)
class personAdmin(admin.ModelAdmin):
    filter_horizontal = ['organizations', 'locations', 'properties',
                         'annotations', 'links']
    list_display = ['name', ]
    list_filter = ['organizations', 'locations']
    inlines = [emailInline, phoneInline, locationInline]

    fieldsets = (
        ('Title', {
            'fields': ('title', 'short_name',)
        }),
        ('Description', {
            'classes': ('collapse',),
            'fields': ['desc', ]
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
            'fields': ['organizations', ]
        }),
    )

@admin.register(models.system_interconnection)
class system_interconnectionAdmin(admin.ModelAdmin):
    filter_vertical = ['interconnection_responsible_roles', 'permitted_protocols']
    list_display = ['external_ip_range','external_organization','external_poc','connection_security','data_direction','desc']
    list_filter = ['external_organization']

    fieldsets = (
        ('Title', {
            'fields': ('title', 'short_name',)
        }),
        ('Description', {
            'fields': ['desc', ]
        }),
        ('Connection', {
            'fields': ('external_ip_range','external_organization','external_poc','connection_security','data_direction',)
        }),
        ('Other', {
            'fields': ('permitted_protocols','interconnection_responsible_roles')
        })
    )

# all other models
models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
