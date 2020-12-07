from scripts.usefullFunctions import *
import json
import os
import shutil

def break_up_catalog(file_path="/Users/dan/PycharmProjects/opal-master/source/"
                     ,file_name="NIST_SP-800-53_rev5-FINAL_catalog.json"):
    """
    Takes an OSCAL Catalog file and breaks it into seperate json files.
    One file is created for each family, control, and enhancement
    family file will contain all controls and control file will contain all enhancements
    so you cna go on to process these at whatever level you want
    """
    startLogging()
    logging.debug("Loading JSON...")
    # file_path = "/Users/dan/PycharmProjects/opal-master/source/"
    # file_name = "NIST_SP-800-53_rev5-FINAL_catalog.json"
    f = file_path + file_name
    shutil.rmtree(file_path + 'tmp')
    os.makedirs(file_path + 'tmp')
    os.makedirs(file_path + 'tmp/byControl')
    os.makedirs(file_path + 'tmp/byFamily')

    catalogDict = json.loads(open(f, 'r').read())
    for group in catalogDict['catalog']['groups']:
        logging.debug("Extracting " + group['title'] + " family...")
        group_file_name = file_path + "tmp/byFamily/" + group.get("id")+".json"
        gf = open(group_file_name,'w')
        json.dump(group,gf,indent=4)
        for control in group['controls']:
            logging.debug("Extracting " + control['title'] + "(" + control['id'] + ") control...")
            control["group_title"] = group["title"]
            control_file_name = file_path + "tmp/byControl/" + control['id']+".json"
            cf = open(control_file_name,'w')
            json.dump(control, cf, indent=4)
            if 'controls' in control:
                logging.debug("Found control enhancements, extracting...")
                for enhancement in control['controls']:
                    logging.debug("Extracting " + control['title'] + " enhancement...")
                    enhancement["group_title"] = group["title"]
                    enhancement_file_name = file_path + "tmp/byControl/" + enhancement['id']+".json"
                    ef = open(enhancement_file_name,'w')
                    json.dump(enhancement,ef, indent=4)

def import_all_controls(path):
    """
    imports all control json files in given directory
    """
    import os

    directory = path
    for filename in os.listdir(directory):
        if filename.endswith(".json") :
            import_individual_control(os.path.join(directory, filename))
        else:
            continue


def save_parameter(id,type,text,depends_on=''):
    param_id, created = t.nist_control_parameter.objects.get_or_create(param_id=id,param_type=type,param_text=text,param_depends_on=depends_on)
    return param_id

def clean_param_text(str):
    str = str.translate(str.maketrans('', '', '\n\t\r')).split(' ')
    while ('' in str):
        str.remove('')
    return ' '.join(str)

def import_individual_control(file_name):
    cntrl = json.loads(open(file_name, 'r').read())
    group_id = cntrl["id"][0:1]
    group_title = cntrl["group_title"]
    parameter_list = []
    cntrl_status = "Active"
    cntrl_label = ""
    cntrl_sortID = ""

    for item in cntrl["properties"]:
        if item["name"] == 'status':
            cntrl_status = item["value"]
        if item["name"] == 'label':
            cntrl_label = item["value"]
        if item["name"] == 'sort-id':
            cntrl_sortID = item["value"]

    control_id, created = t.nist_control.objects.get_or_create(group_id=group_id,
                                         group_title=group_title,
                                         source="NIST SP-800 53 rev5 FINAL",
                                         control_id=cntrl["id"],
                                         control_title=cntrl["title"],
                                         label=cntrl_label,
                                         sort_id=cntrl_sortID,
                                         status=cntrl_status)

    if 'parameters' in cntrl:
        for param in cntrl['parameters']:
            if 'label' in param:
                param_id = save_parameter(param["id"],"label",clean_param_text(param['label']))
            if 'select' in param:
                param_text = ','.join(param['select']['alternatives'])
                param_id = save_parameter(param["id"], "select",clean_param_text(param_text))
            if 'depends-on' in param:
                param_id = save_parameter(param["id"], "label", clean_param_text(param['label']),param["depends-on"])
            t.nist_control.objects.get(pk=control_id.id).parameters.add(param_id)

    if 'parts' in cntrl:
        cntrl_stmnt_text = ''
        logging.debug("Found parts, extracting (better strap in, this could get messy)...")
        for part in cntrl['parts']:
            cntrl_stmnt_text += addControlPart(part)
            cntrl_stmnt, created = t.nist_control_statement.objects.get_or_create(statement_type=part['name'],
                                                                                nist_control_id=control_id.id,
                                                                                statement_text=cntrl_stmnt_text)
            cntrl_stmnt_text = ''


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
    return t

def run():
    break_up_catalog("source/", "NIST_SP-800-53_rev5-FINAL_catalog.json")
    import_all_controls("source/tmp/byControl")