from opal.settings import BASE_DIR
import ssp.models as t
import logging

def startLogging():
    logging.basicConfig(  # filename=logFile,
        filemode='w',
        format='%(name)s - %(levelname)s - %(message)s',
        level=logging.debug()
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


