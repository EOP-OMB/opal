from scripts.usefullFunctions import *
import ssp.models as t
import json
import os
import shutil
import sys

added_nist_controls = 0
updated_nist_controls = 0
control_baseline = t.control_baseline

def break_up_catalog(file_path, file_name):
    """
    Takes an OSCAL Catalog file and breaks it into seperate json files.
    One file is created for each family, control, and enhancement
    family file will contain all controls and control file will contain all enhancements
    so you cna go on to process these at whatever level you want
    """
    startLogging()
    logging.debug("Loading JSON...")

    catalog_source = file_name.replace('.json', '')
    f = file_path
    catalog_dir = BASE_DIR + '/source/tmp/' + catalog_source

    if os.path.isdir(catalog_dir):
        shutil.rmtree(catalog_dir)
    os.makedirs(catalog_dir)

    catalogDict = json.loads(open(f, 'r', encoding='utf8').read())

    for group in catalogDict['catalog']['groups']:
        group_directory_name = catalog_dir + "/" + group.get("id") + "/"
        os.makedirs(group_directory_name)
        # gf = open(group_file_name,'w')
        # json.dump(group,gf,indent=4)
        for control in group['controls']:
            control["group_title"] = group["title"]
            control["catalog"] = catalog_source
            control_file_name = group_directory_name + control['id'] + ".json"
            cf = open(control_file_name, 'w', encoding='utf8')
            json.dump(control, cf, indent=4)
            if 'controls' in control:
                for enhancement in control['controls']:
                    enhancement["group_title"] = group["title"]
                    enhancement["catalog"] = catalog_source
                    enhancement_file_name = group_directory_name + enhancement['id'] + ".json"
                    ef = open(enhancement_file_name, 'w', encoding='utf8')
                    json.dump(enhancement, ef, indent=4)

def import_all_controls(path):
    """
    imports all control json files in given directory
    """
    import os

    control_baseline.controls.clear()
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if name.endswith(".json"):
                import_individual_control(os.path.join(root, name))
        # for name in dirs:
        #     print(os.path.join(root, name))


def save_parameter(id, type, text, nist_control, depends_on=''):
    param_id, created = t.nist_control_parameter.objects.update_or_create(param_id=id, nist_control=nist_control,
                                                                        defaults={'param_id':id,
                                                                        'param_type':type,
                                                                        'param_text':text,
                                                                        'param_depends_on':depends_on,
                                                                        'nist_control':nist_control
                                                                       })
    return param_id


def clean_param_text(str):
    str = str.translate(str.maketrans('', '', '\n\t\r')).split(' ')
    while ('' in str):
        str.remove('')
    return ' '.join(str)


def import_individual_control(file_name):
    logging.debug("Opening file " + file_name)
    cntrl = json.loads(open(file_name, 'r', encoding='utf8').read())
    group_id = str(cntrl["id"][0:2]).upper()
    group_title = cntrl["group_title"]
    cntrl_catalog = cntrl["catalog"]
    parameter_list = []
    cntrl_status = "Active"
    cntrl_label = ""
    cntrl_sortID = ""
    global added_nist_controls, updated_nist_controls


    for item in cntrl["properties"]:
        if item["name"] == 'status':
            cntrl_status = item["value"]
        if item["name"] == 'label':
            cntrl_label = item["value"]
        if item["name"] == 'sort-id':
            cntrl_sortID = item["value"]

    control_id, created = t.nist_control.objects.update_or_create(group_id=group_id,
                                                               group_title=group_title,
                                                               source=cntrl_catalog,
                                                               control_id=cntrl["id"],
                                                               defaults={'group_id':group_id,
                                                                    'group_title':group_title,
                                                                    'source':cntrl_catalog,
                                                                    'control_id':cntrl["id"],
                                                                    'control_title':cntrl["title"],
                                                                    'label':cntrl_label,
                                                                    'sort_id':cntrl_sortID,
                                                                    'status':cntrl_status,
                                                                    'catalog':cntrl_catalog
                                                               })

    control_baseline.controls.add(control_id)

    if not created:
        logging.debug("Found existing entry for " + cntrl["title"] + " from catalog " + cntrl_catalog)
        updated_nist_controls += 1

    else:
        logging.debug("No existing entry for " + cntrl["title"] + "from catalog " + cntrl_catalog + " found. Created New entry.")
        added_nist_controls += 1



    if 'parameters' in cntrl:
        for param in cntrl['parameters']:
            param_id = None
            if 'label' in param:
                if 'depends-on' in param:
                    param_id = save_parameter(param["id"], "label", clean_param_text(param['label']), control_id,
                                              param["depends-on"])
                else:
                    param_id = save_parameter(param["id"], "label", clean_param_text(param['label']), control_id)
            if 'select' in param:
                param_text = ','.join(param['select']['alternatives'])
                param_id = save_parameter(param["id"], "select", clean_param_text(param_text), control_id)


    if 'parts' in cntrl:
        cntrl_stmnt_text = ''
        logging.debug("Found parts, extracting (better strap in, this could get messy)...")
        for part in cntrl['parts']:
            cntrl_stmnt_text += addControlPart(part)
            t.nist_control_statement.objects.get_or_create(statement_type=part['name'],
                                                            nist_control_id=control_id.id,
                                                            statement_text=cntrl_stmnt_text)
            cntrl_stmnt_text = ''


def addControlPart(part, indent=0):
    t = ''
    logging.debug("Extracting Part...")
    if 'title' in part:
        logging.debug("Found part Title...")
        t = "<b>" + part['title'] + "<b>"
        logging.debug("Title added...")
    if 'properties' in part:
        logging.debug("Found properties, extracting...")
        for p in part['properties']:
            if p['name'] == 'label':
                t += '<br>\n' + str('&nbsp;' * indent) + p['value'] + ' '
            logging.debug("Property added...")
    if 'prose' in part:
        logging.debug("Found prose, extracting...")
        t += part['prose']
        logging.debug("Prose added...")
    if 'parts' in part:
        for subpart in part['parts']:
            logging.debug("Found subpart, extracting...")
            t += addControlPart(subpart, indent + 2)
            logging.debug("Added subpart...")
    return t


def run(catalog_control_baseline, file_path=BASE_DIR + '/source/NIST_SP-800-53_rev4_catalog.json', file_name='NIST_SP-800-53_rev4_catalog.json'):
    global added_nist_controls, updated_nist_controls, control_baseline
    added_nist_controls = updated_nist_controls = 0
    control_baseline = catalog_control_baseline

    break_up_catalog(file_path, file_name)
    #break_up_catalog(BASE_DIR + '/source/', "NIST_SP-800-53_rev5-FINAL_catalog.json")
    import_all_controls(BASE_DIR + '/source/tmp/' + file_name.replace('.json', ''))
    return added_nist_controls, updated_nist_controls

#Samira: Modified this file to use it in import_catalog view which imports one catalog file at a time.

