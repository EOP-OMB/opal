import logging
from datetime import datetime
from os import path

from django.conf import settings

from catalog.models import controls
from component.models import by_components, implemented_requirements, components
from real_data.controls_dict import ctr_list

# create logger
logger = logging.getLogger('console_log')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


def import_statements():
    """
    Imports a set of control statements exported from opal_v1
    """
    skip_list = []

    new_component = components.objects.create(type="this-system",title="Imported Control Set " + datetime.now().isoformat(),purpose="Import",status="other")

    logger.info("Starting import process...")
    for ctrl in ctr_list:
        # profile_id = ctrl['profile']
        logger.info("Looking for control with sort-id " + ctrl['control_sort_id'])
        if controls.objects.filter(props__value=ctrl['control_sort_id'], props__name='sort-id').exists():
            control_uuid = controls.objects.get(props__value=ctrl['control_sort_id'],props__name='sort-id')
            logger.info("Found control, id: " + str(control_uuid.id))
            desc = ""
            logger.info("Building description...")
            for i in ctrl['description']:
                desc += i['statement_id'] + ": " + i["text"] + "\n\n"
            logger.info("Description done. ")
            logger.info("Creating new by_component")
            new_by_comp = by_components(component_uuid_id=new_component.id, description=desc, implementation_status=ctrl['implementation_status'])
            new_by_comp.save()
            logger.info("New by_component saved")
            logger.info("Creating new implimented_requirement")
            new_implimented_requirement = implemented_requirements(control_id=control_uuid)
            new_implimented_requirement.save()
            logger.info("New implemented_requirement saved")
            logger.info("Adding implemented_requirement to new by_component")
            new_implimented_requirement.by_components.add(new_by_comp)
            new_implimented_requirement.save()
            logger.info("Done, looping to next control...")
        else:
            skip_list.append(ctrl)
            logger.info("Could not find control with sort-id " + ctrl['control_sort_id'] + '. Skipping...')
    #output_file_name = path.join(settings.BASE_DIR,"real_data","skipped_ctrls.py")
    #output_file = open(output_file_name,'w')
    #output_file.write("ctrl_list=" + str(skip_list))
    #output_file.close()
    return skip_list



