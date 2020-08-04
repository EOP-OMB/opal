from scripts.usefullFunctions import *


def addControlBase(group_id, group_title, control):
    logging.debug("Creating control " + control['id'])
    newControl, created = nist_control.objects.get_or_create(group_id=group_id, group_title=group_title,
                                                             control_id=control['id'], source=control['class'],
                                                             control_title=control['title'])
    return newControl


def saveControlParam(p):
    newParameter, created = nist_control_parameter.objects.get_or_create(param_id=p['parameter_id'],
                                                                         param_text=p['parameter_text'],
                                                                         param_type=p['parameter_type'],
                                                                         param_class=p['parameter_class'],
                                                                         param_depends_on=p['parameter_depends_on'])
    logging.debug("Save complete...")
    return newParameter.id


def addControlParam(parameter):
    logging.debug("Extracting Parameter " + parameter['id'])
    p = {'parameter_id': parameter['id']}
    if 'class' in parameter:
        p['parameter_class'] = parameter['class']
    else:
        p['parameter_class'] = ''
    if 'depends-on' in parameter:
        p['parameter_depends_on'] = parameter['depends-on']
    else:
        p['parameter_depends_on'] = ''
    if 'label' in parameter:
        p['parameter_text'] = parameter['label']
        p['parameter_type'] = 'label'
    if 'descriptions' in parameter:
        for description in parameter:
            p['parameter_text'] = description['summary']
            p['parameter_type'] = 'description'
    if 'constraints' in parameter:
        for constraint in parameter['constraints']:
            p['parameter_text'] = constraint['detail']
            p['parameter_type'] = 'constraint'
    if 'guidance' in parameter:
        for guideline in parameter['guidance']:
            p['parameter_text'] = guideline['prose']
            p['parameter_type'] = 'guidance'
    if 'value' in parameter:
        p['parameter_text'] = parameter['value']
        p['parameter_type'] = 'value'
    if 'select' in parameter:
        for alternatives in parameter['select']:
            for choice in alternatives:
                p['parameter_text'] = choice
                p['parameter_type'] = 'select'
    logging.debug("Saving parameter...")
    controlParameter = saveControlParam(p)
    return controlParameter


def addControlProperties(p, newControl):
    logging.debug("adding property: " + p['name'])
    if p['name'] == 'label':
        logging.debug("Adding Label...")
        newControl.label = p['value']
    elif p['name'] == 'sort-id':
        logging.debug("Adding sort_id...")
        newControl.sort_id = p['value']
    elif p['name'] == 'status':
        logging.debug("Adding status...")
        newControl.status = p['value']
    else:
        logging.error("No instructions for property of type " + p['name'] + ', skipping...')
    newControl.save()
    return p['name']


def addLink(text, href, rel):
    """
    This isn't working right now
    """
    logging.debug("adding link...")
    newLink = link.objects.create(text=text, href=href, rel=rel)
    newLink.save()
    logging.debug("Link added")
    return newLink.uuid


def addControlPart(part, indent=0):
    t = ''
    logging.debug("Extracting Part...")
    if 'title' in part:
        logging.debug("Found part Title...")
        t = "<b>" + part['title'] + "<b>"
    if 'properties' in part:
        logging.debug("Found properties, extracting...")
        for p in part['properties']:
            if p['name'] == 'label':
                t += '<br>\n' + str('&nbsp;' * indent) + p['value'] + ' '
            logging.debug("Property added...")
    if 'prose' in part:
        logging.debug("Found prose, extracting...")
        t += part['prose']
    if 'parts' in part:
        for subpart in part['parts']:
            logging.debug("Found subpart, extracting...")
            t += addControlPart(subpart, indent + 2)
            logging.debug("Added subpart...")
    # This isn't working right now
    # TODO: Fix links
    # if 'links' in part:
    #     logging.debug("Found links, extracting...")
    #     for link in part['links']:
    #         if 'href' in link:
    #             href = link['href']
    #         else:
    #             href = ''
    #         if 'rel' in link:
    #             rel = link['rel']
    #         else:
    #             rel = ''
    #         l = addLink(link['text'],href,rel)
    #         newPart.links.add(l)
    #         logging.debug("Added Link...")
    return t


def addNewControl(group_id, group_title, control):
    logging.debug("Adding basic control elements...")
    newControl = addControlBase(group_id, group_title, control)
    ncs = ''
    if 'parameters' in control:
        logging.debug('Found parameters, extracting...')
        for parameter in control['parameters']:
            newParameter = addControlParam(parameter)
            newControl.parameters.add(newParameter)
    if 'properties' in control:
        logging.debug("Found properties, extracting...")
        for p in control['properties']:
            addControlProperties(p, newControl)
    if 'annotations' in control:
        logging.debug("Found Annotations...")
        for a in control['annotations']:
            annotation_name = a['name']
            if 'id' in a:
                annotation_id = a['id']
            else:
                annotation_id = None
            if 'ns' in a:
                annotation_ns = a['ns']
            else:
                annotation_ns = None
            if 'value' in a:
                annotation_value = a['value']
            else:
                annotation_value = None
            if 'remarks' in a:
                annotation_remarks = a['remarks']
            else:
                annotation_remarks = None
            newAnnotation = annotation.objects.get_or_create(name=annotation_name, annotationID=annotation_id,
                                                             ns=annotation_ns, value=annotation_value,
                                                             remarks=annotation_remarks)
            newControl.annotations.add(newAnnotation)
    # This is also not working right now
    # TODO: Fix links
    # if 'links' in control:
    #     logging.debug("Found links, extracting...")
    #     for l in control['links']:
    #         newControl.links.add(addLink(l['text'],l['href'],l['rel']))
    if 'parts' in control:
        logging.debug("Found parts, extracting (better strap in, this could get messy)...")
        for part in control['parts']:
            ncs += addControlPart(part)
            newStatement, created = nist_control_statement.objects.get_or_create(statement_type=part['name'],control_id=control['id'])
            newStatement.statement_text = ncs
            ncs = ''
            newStatement.save()
            newControl.control_statements.add(newStatement.id)

    # newControl.nist_control_guidance = newControl.statement_view('guidance')
    # newControl.nist_control_objectives = newControl.statement_view('objectives')
    # newControl.nist_control_objects = newControl.statement_view('objects')
    newControl.save()
    if 'controls' in control:
        logging.debug("Found control enhancements, extracting...")
        for enhancement in control['controls']:
            addNewControl(group_id, group_title, enhancement)


def cleanNISTControls():
    """
    Deletes all NIST Control objects from the database
    """
    # nist_control.objects.all().delete()
    pass


def loadControls(f):
    import json
    startLogging()
    logging.debug("Clearing all NIST Control Tables...")
    logging.debug("Loading JSON...")
    catalogDict = json.loads(open(f, 'r').read())
    for group in catalogDict['catalog']['groups']:
        logging.debug("Extracting " + group['title'] + " family...")
        for control in group['controls']:
            logging.debug("Extracting " + control['title'] + "(" + control['id'] + ") control...")
            addNewControl(group['id'], group['title'], control)
            if 'controls' in control:
                logging.debug("Found control enhancements, extracting...")
                for enhancement in control['controls']:
                    logging.debug("Extracting " + control['title'] + " enhancement...")
                    addNewControl(group['id'], group['title'], enhancement)


def run():
    f='/Users/dan/PycharmProjects/opal/source/NIST_SP-800-53_rev4_catalog.json'
    loadControls(f)