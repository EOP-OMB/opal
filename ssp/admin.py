from django.contrib import admin
from django.apps import apps
from ssp import models

# These are some useful functions for cleaning up data after an import
def changeRoll(old_role,new_role):
    controls = models.system_control.objects.filter(responsibleRoles=models.user_role.objects.filter(title=old_role)[0].pk)
    for item in controls:
        item.responsibleRoles.add(models.user_role.objects.filter(title=new_role)[0].pk)
        item.responsibleRoles.remove(models.user_role.objects.filter(title=old_role)[0].pk)
    models.user_role.objects.filter(title=old_role)[0].delete()

def delUnusedRoles():
    r = models.user_role.objects.all()
    for item in r:
        if item.system_control_set.count() == 0:
            print('deleting ' + item.title)
            item.delete()


def listRolesWithControlCount():
    r = models.user_role.objects.all()
    role_dictionary = {}
    for role in r:
        role_dictionary[role.title] = role.control_statement_set.count()
    sort_roles = sorted(role_dictionary.items(), key=lambda x: x[1], reverse=True)

    for i in sort_roles:
        print(i[0], i[1])

# Register your models here.

@admin.register(models.system_security_plan)
class systemSecurityPlanAdmin(admin.ModelAdmin):
    filter_horizontal = ['system_components','system_services','system_interconnections','system_inventory_items','controls','properties','links']

    def __str__(self):
        return "System Security Plans (SSPs)"

@admin.register(models.system_control)
class system_controlAdmin(admin.ModelAdmin):
    filter_horizontal = ['control_responsible_roles','control_parameters','control_statements','properties','annotations','links']
    list_filter = ['control_responsible_roles','control_origination','nist_control__group_title']
    list_display = ['nist_control']
    sortable_by = ['sort_id']

@admin.register(models.control_statement)
class control_statementAdmin(admin.ModelAdmin):
    filter_horizontal = ['control_statement_responsible_roles','properties','links','annotations']

@admin.register(models.nist_control)
class nist_controlAdmin(admin.ModelAdmin):
    filter_horizontal = ['parameters']
    list_filter = ['group_title']
    list_display = ['group_id','group_title','control_id','label']
    list_display_links = ['group_id','group_title','control_id','label']

@admin.register(models.system_inventory_item)
class system_inventory_itemAdmin(admin.ModelAdmin):
    filter_horizontal = ['properties', 'links', 'annotations']
    list_filter = ['inventory_item_type']
    list_display = ['item_id', 'inventory_item_type', 'item_description']

@admin.register(models.inventory_item_type)
class inventory_item_typeAdmin(admin.ModelAdmin):
    filter_horizontal = ['responsibleRoles','properties', 'links', 'annotations']
    list_display = ['inventory_item_type_name', 'use', 'description', 'baseline_configuration']

@admin.register(models.system_interconnection)
class system_interconnectionAdmin(admin.ModelAdmin):
   filter_horizontal =  ['interconnection_responsible_roles','properties', 'links', 'annotations']

@admin.register(models.link)
class linkAdmin(admin.ModelAdmin):
    list_display = ['text','href','mediaType','requires_authentication']
    list_editable = ['text','href','mediaType','requires_authentication']
    list_display_links = None

@admin.register(models.system_service)
class system_serviceAdmin(admin.ModelAdmin):
    list_display = ['service_title','service_description']
    filter_horizontal = ['protocols','service_information_types','properties','annotations','links']
    list_filter = ['protocols']

@admin.register(models.system_component)
class system_componentAdmin(admin.ModelAdmin):
    filter_horizontal = ['component_information_types','component_responsible_roles','properties','annotations','links']
    list_filter = ['component_information_types','component_status','component_responsible_roles','component_type']
    list_display = ['component_title','component_type', 'component_description']

@admin.register(models.system_characteristic)
class system_characteristicAdmin(admin.ModelAdmin):
    list_display = ['system_name','system_status']
    filter_horizontal = ['properties','annotations','links','leveraged_authorizations']

@admin.register(models.person)
class personAdmin(admin.ModelAdmin):
    filter_horizontal = ['organizations','locations','email_addresses','telephone_numbers','properties','annotations','links']
    list_display = ['name',]
    list_filter = ['organizations','locations']

@admin.register(models.organization)
class organizationAdmin(admin.ModelAdmin):
    filter_horizontal = ['locations', 'email_addresses', 'telephone_numbers', 'properties','annotations', 'links']

# all other models
models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass