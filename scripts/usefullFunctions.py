from opal.settings import BASE_DIR
import ssp.models as t
import logging
from rest_framework.renderers import JSONRenderer
import json

def startLogging():
    logging.basicConfig(  # filename=logFile,
        filemode='w',
        format='%(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG
    )

def addControlsToGroup(group_name,controls):
    """
    :param group_name: The name of a new group of controls. Cold be a new baseline or a common set of controls such as those addressed by a particular component
    :param controls: a list object contining one or more system_control objects
    """
    from ssp.models import element_property, system_control
    p = element_property.objects.get_or_create(ns='control_group', name=group_name, value='true')
    for item in controls:
        item.properties.add(p[0])
        item.save()


# These are some useful functions for cleaning up data after an import
def changeRoll(old_role,new_role):
    from ssp.models import system_control, user_role
    controls = system_control.objects.filter(responsibleRoles=user_role.objects.filter(title=old_role)[0].pk)
    for item in controls:
        item.responsibleRoles.add(user_role.objects.filter(title=new_role)[0].pk)
        item.responsibleRoles.remove(user_role.objects.filter(title=old_role)[0].pk)
    user_role.objects.filter(title=old_role)[0].delete()

def delUnusedRoles():
    from ssp.models import user_role
    r = user_role.objects.all()
    for item in r:
        if item.system_control_set.count() == 0:
            print('deleting ' + item.title)
            item.delete()


def listRolesWithControlCount():
    from ssp.models import user_role
    r = user_role.objects.all()
    role_dictionary = {}
    for role in r:
        role_dictionary[role.title] = role.control_statement_set.count()
    sort_roles = sorted(role_dictionary.items(), key=lambda x: x[1], reverse=True)

    for i in sort_roles:
        print(i[0], i[1])

def linkSystemControltoNISTControl(catalog):
    from ssp.models.controls import system_control, nist_control
    logging.debug("Stsrting...")
    for item, key in system_control.objects.all().values_list('nist_control', 'pk'):
        control = system_control.objects.get(pk=key)
        logging.debug('Opened control ' + control.title)
        nist_control_id = control.short_name
        logging.debug('Looking up ' + nist_control_id)
        try:
            control.nist_control = nist_control.objects.get(sort_id=nist_control_id,catalog=catalog)
            control.save()
            logging.debug('Found nist control, link established')
        except nist_control.DoesNotExist:
            logging.debug(nist_control_id + ' not found')


def createFixtures():
    import os
    from django.apps import apps

    fixture_dir = os.path.join(BASE_DIR, 'ssp/fixtures/')

    app_models = apps.get_app_config('ssp').get_models()
    for model in app_models:
        if len(model.objects.all()) > 0:
            cmd = 'python manage.py dumpdata ssp.' + model.__name__ + ' --natural-foreign --natural-primary -o ' + fixture_dir + model.__name__ + '.json'
            os.system(cmd)

def serializerJSON(data, SSP=False):
    json_data = JSONRenderer().render(data)
    json_object = json.loads(json_data)
    json_str = json.dumps(json_object, indent=2)
    return aliasOSCAL(json_str, SSP=OSCAL)

def aliasOSCAL(json_str, SSP=False):
    json_str = json_str.replace('"short_name":', '"short-name":')
    json_str = json_str.replace('"telephone_numbers:"', '"telephone-numbers":')
    json_str = json_str.replace('"email_addresses":', '"email-addresses":')
    json_str = json_str.replace('"lastModified":', '"last-modified":')
    json_str = json_str.replace('"oscalVersion":', '"oscal-version":')
    json_str = json_str.replace('"desc":', '"description":')
    json_str = json_str.replace('Impact":', '-impact":')
    json_str = json_str.replace('"system-status":', '"status":')
    json_str = json_str.replace('"authorization_boundary_diagram":', '"authorization-boundary":')
    json_str = json_str.replace('"network_architecture_diagram":', '"network-architecture":')
    json_str = json_str.replace('"data_flow_diagram":', '"data-flow":')
    json_str = json_str.replace('"leveraged_authorization":', '"leveraged-authorizations":')
    json_str = json_str.replace('"system_users":', '"users":')
    json_str = json_str.replace('"system_components":', '"components":')
    json_str = json_str.replace('"system_inventory_items":', '"inventory-items":')
    json_str = json_str.replace('"system_characteristics":', '"system-characteristics":')
    json_str = json_str.replace('"date_authorized":', '"date-authorized":')
    json_str = json_str.replace('"security_sensitivity_level":', '"security-sensitivity-level":')
    json_str = json_str.replace('"system_information":', '"system-information":')
    json_str = json_str.replace('"information_types":', '"information-types":')
    json_str = json_str.replace('"security_impact_level":', '"security-impact-level":')
    json_str = json_str.replace('"security_objective_confidentiality":', '"security-objective-confidentiality":')
    json_str = json_str.replace('"security_objective_integrity":', '"security-objective-integrity":')
    json_str = json_str.replace('"security_objective_availability":', '"security-objective-availability":')
    json_str = json_str.replace('"system_status":', '"system-status":')
    json_str = json_str.replace('"system_implementation":', '"system-implementation":')
    json_str = json_str.replace('"component_type":', '"component-type":')
    json_str = json_str.replace('"component_title":', '"component-title":')
    json_str = json_str.replace('"component_description":', '"component-description":')
    json_str = json_str.replace('"component_information_types":', '"component-information-types":')
    json_str = json_str.replace('"component_status":', '"component-status":')
    json_str = json_str.replace('"component_responsible_roles":', '"component-responsible-roles":')
    json_str = json_str.replace('"control_implementation":', '"control-implementation":')
    json_str = json_str.replace('"control_parameters":', '"parameter-settings":')
    json_str = json_str.replace('"control_statements":', '"statements":')
    json_str = json_str.replace('"system_name":', '"system-name":')
    if SSP:
        json_str = json_str.replace('"controls": [', '"implemented-requirements": [')
        json_str = json_str.replace('"properties":', '"props":')
    return json_str


