import json
from ssp.models import system_security_plan

def objToDictionary(key_value_list, obj):
    if not obj.exists():
        return None
    else:
        return_list = []
        for item in obj:
            dict = {}
            for i in key_value_list:
                dict[i[0]] = getattr(item, i[1])
            return_list.append(dict)
        return return_list


def getProperties(obj):
    dk = [
        ['value', 'value'],
        ['name', 'name'],
        ['uuid', 'property_id'],
        ['ns', 'ns'],
        ['class', 'prop_class']
    ]
    return objToDictionary(dk,obj)


def getLinks(obj):
    dk = [
        ['text', 'text'],
        ['href', 'href'],
        ['rel', 'rel'],
        ['media-type', 'mediaType']
    ]
    return objToDictionary(dk, obj)


def getAnnotations(obj):
    dk = [
        ['name','name'],
        ['uuid', 'annotationID'],
        ['ns', 'ns'],
        ['value', 'value'],
        ['remarks', 'remarks']
    ]
    return objToDictionary(dk, obj)


def getRoles(obj):
    dk = [['id', 'id'],
          ['title', 'title'],
          ['short-name', 'shortName'],
          ['desc', 'desc']]
    dict = objToDictionary(dk, obj)
    dict['properties'] = getProperties(obj.properties.all())
    dict['annotations'] = getAnnotations(obj.annotations.all())
    dict['links'] = getLinks(obj.links.all())
    dict['remarks'] = obj.remarks
    return dict


def getInformationTypes(obj):
    if not obj.exists():
        return None
    else:
        info_types_list = []
        for i in obj:
            info_type = {
                'uuid': i.id,
                'title': i.system_information_type_name,
                'description': i.information_type.description,
                'confidentiality-impact': {
                    'base': i.information_type.confidentialityImpact,
                    'selected': i.adjusted_confidentiality_impact,
                    'adjusted-justification': i.adjusted_confidentiality_impact_justification
                },
                'integrity-impact': {
                    'base': i.information_type.integrityImpact,
                    'selected': i.adjusted_integrity_impact,
                    'adjusted-justification': i.adjusted_integrity_impact_justification
                },
                'availability-impact': {
                    'base': i.information_type.availabilityImpact,
                    'selected': i.adjusted_availability_impact,
                    'adjusted-justification': i.adjusted_availability_impact_justification
                }
            }
            info_types_list.append(info_type)
        return info_types_list

def getLeveragedAuthorizations(obj):
    if not obj.exists():
        return None
    else:
        leveraged_authorizations_list = []
        for a in obj:
            auth = {
                'uuid': obj.id,
                'title': obj.leveraged_system_name,
                'party-uuid': '', #TODO add party uuid to leveraged_authorization model
                'date_authorized': '', #TODO add date authorized to leveraged_authorization model
            }
            leveraged_authorizations_list.append(auth)
        return leveraged_authorizations_list


def getAuthorizedPrivileges(obj):
    if not obj.exists():
        return None
    else:
        authorized_privleges_list = []
        for a in obj:
            auth = {
                'title': a.title,
                'description': a.description,
                'functions-performed': a.functionsPerformed.all().values
            }
            authorized_privleges_list.append(auth)
        return authorized_privleges_list



def getSystemImplementation(authorizations,users,components):
    dict_obj = {'leveraged-authorizations': getLeveragedAuthorizations(authorizations),
            }
    for r in users:
        dict_obj[r.id] = {
            'title': r.user.name,
            'short-name': r.user.short_name,
            'role-ids': r.roles.all().values,
            'authorized-privileges': getAuthorizedPrivileges(r.roles.user_privileges.all())
            }
    return dict_obj

def main(ssp_id=1, output_file='default'):
    ssp = system_security_plan.objects.get(pk=ssp_id)
    if output_file == 'default':
        output_file = ssp.title.replace(' ', '_') + '.json'
    system_security_plan_json = {
        'uuid': ssp.sspID,
        'metadata': {
            'title': ssp.title,
            'published': ssp.published.strftime('%Y-%m-%d %h:%M %Z'),
            'last_modified': ssp.lastModified.strftime('%Y-%m-%d %h:%M %Z'),
            'version': ssp.version,
            'oscal-version': ssp.oscalVersion,
            'properties': getProperties(ssp.properties.all()),
            'links': getLinks(ssp.links.all()),
            'remarks': ssp.remarks,
        },
        'system-characteristics': {
            'system-ids': ssp.system_characteristics.id,
            'system-name': ssp.system_characteristics.system_name,
            'system-name-short': ssp.system_characteristics.system_short_name,
            'description': ssp.system_characteristics.system_description,
            'properties': getProperties(ssp.system_characteristics.properties.all()),
            'annotations': getAnnotations(ssp.system_characteristics.annotations.all()),
            'links': getLinks(ssp.system_characteristics.links.all()),
            'date-authorized': ssp.system_characteristics.date_authorized,
            'security-sensitivity-level': ssp.system_characteristics.security_sensitivity_level,
            'system-information': {
                'information-types': getInformationTypes(ssp.system_characteristics.system_information.all())},
            'security-impact-level': {
                'security-impact-level': {
                    'security-objective-confidentiality': ssp.system_characteristics.security_objective_confidentiality,
                    'security-objective-integrity': ssp.system_characteristics.security_objective_integrity,
                    'security-objective-availability': ssp.system_characteristics.security_objective_availability},
                'status': {'state': ssp.system_characteristics.system_status.state},
                'authorization-boundary': {
                    'properties': getProperties(ssp.system_characteristics.authorization_boundary_diagram.properties.all()),
                    'annotations': getAnnotations(
                        ssp.system_characteristics.authorization_boundary_diagram.annotations.all()),
                    'links': getLinks(ssp.system_characteristics.authorization_boundary_diagram.links.all()),
                    ssp.system_characteristics.authorization_boundary_diagram_id: {
                        'description': ssp.system_characteristics.authorization_boundary_diagram.description,
                        'caption': ssp.system_characteristics.authorization_boundary_diagram.caption,
                    },
                    'remarks': ssp.system_characteristics.authorization_boundary_diagram.remarks
                },
                'network-architecture': {
                    'properties': getProperties(ssp.system_characteristics.network_architecture_diagram.properties.all()),
                    'annotations': getAnnotations(
                        ssp.system_characteristics.network_architecture_diagram.annotations.all()),
                    'links': getLinks(ssp.system_characteristics.network_architecture_diagram.links.all()),
                    ssp.system_characteristics.network_architecture_diagram_id: {
                        'description': ssp.system_characteristics.network_architecture_diagram.description,
                        'caption': ssp.system_characteristics.network_architecture_diagram.caption,
                    },
                    'remarks': ssp.system_characteristics.network_architecture_diagram.remarks
                },
                'data-flow': {
                    'properties': getProperties(ssp.system_characteristics.data_flow_diagram.properties.all()),
                    'annotations': getAnnotations(
                        ssp.system_characteristics.data_flow_diagram.annotations.all()),
                    'links': getLinks(ssp.system_characteristics.data_flow_diagram.links.all()),
                    ssp.system_characteristics.data_flow_diagram_id: {
                        'description': ssp.system_characteristics.data_flow_diagram.description,
                        'caption': ssp.system_characteristics.data_flow_diagram.caption,
                    },
                    'remarks': ssp.system_characteristics.data_flow_diagram.remarks
                },
                'remarks': ssp.system_characteristics.remarks
            }
        },
        'system-implementation': getSystemImplementation(
            ssp.system_characteristics.leveraged_authorizations.all(),
            ssp.system_users.all(),
            ssp.system_components.all()
        ),
        'control-implementation': ''
    }

    f = open(output_file, 'w')
    f.write(json.dumps(system_security_plan_json,indent=2))
    return 'ssp exported to ' + output_file
