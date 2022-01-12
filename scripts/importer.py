from ssp.models.systems import *
from scripts.usefullFunctions import *


def load_ssp():
    startLogging()

    # load the OSCAL SSP JSON
    oscal = open('/Users/dan/Projects/omb/atlasify/oscal-ssp-import/GovReady/govready-ssp-oscal-01.json', 'r',encoding='utf-8-sig')
    # oscal = open('GovReady/govready-ssp-oscal-cmpt-ubuntu-16.04-ac-10-01.json', 'r', encoding='utf-8-sig')
    # oscal = open('GovReady/govready-ssp-ubuntu-16.04-lts-oscal.json', 'r', encoding='utf-8-sig')
    oscal_data = json.load(oscal)

    # begin processing OSCAL data and get the level 1 data
    level_1 = oscal_data["system-security-plan"]

    # create the ssp object
    ssp, created = system_security_plan.objects.get_or_create(uuid=level_1["uuid"])

    #############################################################################################
    # METADATA SECTION
    #############################################################################################
    meta = level_1["metadata"]
    ssp.title = meta["title"]
    if "published" in meta:
        ssp.published = meta["published"]
    ssp.updated_at = meta["last-modified"]
    ssp.version = meta["version"]
    ssp.oscalVersion = meta["oscal-version"]
    if "remarks" in meta:
        ssp.remarks = meta["remarks"]
    ssp.save()
    # get the properties
    if "properties" in meta:
        props = meta["properties"]
        for prop in props:
            p, created = element_property.objects.create(name=prop["name"], value=prop["value"])
            ssp.properties.add(p.id)
    # TODO skipping revision history for now
    # get the revision history
    # if "revision-history" in meta:
    #     hist = meta["revision-history"]
    #     ssp["Description"] += "<br/><h4>Revision History</h4>"
    #     for i in hist:
    #         ssp["Description"] += "Version: " + i["version"] + ", Date Published: " + i["published"] + ", OSCAL Version: " + \
    #                               i["oscal-version"] + ", Remarks: " + i["remarks"] + "<br/>"
    # get the roles
    if "roles" in meta:
        roles = meta["roles"]
        for role in roles:
            r, created = user_role.objects.get_or_create(title=role["title"],short_name = role["id"])
            if "desc" in role:
                r.desc = role["desc"]
            r.save()
    # TODO: import locations
    # create a dictionary for locations
    # if "locations" in meta:
    #     locations = meta["locations"]

    #############################################################################################
    # PROFILE SECTION TODO: skipping profile import for now
    #############################################################################################
    # prof = level_1["import-profile"]
    # ssp["Description"] += "<br/><h4>OSCAL Profile</h4>"
    # for i in prof:
    #     ssp["Description"] += "Imported: " + prof["href"] + "<br/>"

    #############################################################################################
    # SYSTEM CHARACTERISTICS
    #############################################################################################
    chars = level_1["system-characteristics"]
    ssp.short_name = chars['system-name-short']
    other_ids = chars["system-ids"]
    int_loop = 0
    for role in other_ids:
        ssp.remarks += "Other System Identifiers\n"
        if int_loop != 0:
            ssp.remarks += ", "
        ssp.remarks += role["id"]
        int_loop += 1
    # get system descriptions
    ssp.desc = chars["description"]
    # overall categorization
    # TODO: setting the security_impact_level is returning an error, need to fix that
    # ssp.security_impact_level = chars["security-sensitivity-level"]
    # process properties
    if "properties" in chars:
        system_component_properties = chars["properties"]
        if len(system_component_properties) > 0:
            for role in system_component_properties:
                p, created = element_property.objects.get_or_create(name=role["name"], value=role["value"])
                ssp.properties.add(p.id)
    # process annotations
    if "annotations" in chars:
        system_component_annotations = chars["annotations"]
        if len(system_component_annotations) > 0:
            for role in system_component_annotations:
                a, created = annotation.objects.get_or_create(title=role["name"], value=role["value"], remarks=role["remarks"])
                ssp.annotations.add(a.id)
    # process system information
    scInfo = chars["system-information"]
    if "properties" in scInfo:
        scInfoProps = scInfo["properties"]
        for role in scInfoProps:
            p, created = element_property.objects.get_or_create(name=role["name"], value=role["value"])
            ssp.properties.add(p.id)
    # process information types
    scInfoTypes = scInfo["information-types"]
    for role in scInfoTypes:
        info_type, created = information_type.objects.get_or_create(title=role["title"], desc=role["description"],
                                                           confidentialityImpact=role["confidentiality-impact"]["base"],
                                                           integrityImpact=role["integrity-impact"]["base"],
                                                           availabilityImpact=role["availability-impact"]["base"])
        ssp.information_types.add(info_type.id)
    # process security impact level
    scLevels = chars["security-impact-level"]

    security_levels_mapping = {"fips-199-high": "High", "fips-199-moderate": "Moderate", "fips-199-low": "Low","UNKNOWN":"UNKNOWN"}

    ssp.security_objective_confidentiality = security_levels_mapping[scLevels["security-objective-confidentiality"]]
    ssp.security_objective_integrity = security_levels_mapping[scLevels["security-objective-integrity"]]
    ssp.security_objective_availability = security_levels_mapping[scLevels["security-objective-availability"]]

    # get the status
    stat = chars["status"]
    ssp.system_status, created = status.objects.get_or_create(state=stat["state"])
    # TODO import authorization boundary, network architecture, and data flow
    # process authorization boundary, network architecture, and data flow
    # authb = chars["authorization-boundary"]
    # ssp["AuthorizationBoundary"] += authb["description"]
    # if "network-architecture" in chars:
    #     netx = chars["network-architecture"]
    #     ssp["NetworkArchitecture"] += netx["description"]
    # if "data-flow" in chars:
    #     df = chars["data-flow"]
    #     ssp["DataFlow"] += df["description"]

    #############################################################################################
    # SYSTEM IMPLEMENTATION
    #############################################################################################
    imps = level_1["system-implementation"]
    # process properties
    if "props" in imps:
        impProps = imps["props"]
        for role in impProps:
            if "value" in role:
                p, created = element_property.objects.get_or_create(name=role["name"], value=role["value"])
                ssp.properties.add(p.id)
    # TODO: process users
    # scUsers = imps["users"]
    # for i in scUsers:
    #
    #     scUser = scUsers[i]
    #
    #     userTable += "<td>" + scUser["title"] + " (GUID: " + i + ")</td>"
    #     # get user properties
    #     strUserProp = "<td>"
    #     if "props" in scUser:
    #         scUserProps = scUser["props"]
    #         for i in scUserProps:
    #             strUserProp += i["name"] + ": " + i["value"] + "<br/>"
    #     if "annotations" in scUser:
    #         scUserAnno = scUser["annotations"]
    #         for i in scUserAnno:
    #             strUserProp += i["name"] + ": " + i["value"] + "<br/>"
    #     strUserProp += "</td>"
    #     userTable += strUserProp
    #     # get user roles
    #     if "role-ids" in scUser:
    #         scRoles = scUser["role-ids"]
    #         strUserRoles = "<td>"
    #         for i in scRoles:
    #             strUserRoles += i + "<br/>"
    #         strUserRoles += "</td>"
    #     else:
    #         strUserRoles = "<td></td>"
    #     userTable += strUserRoles
    #     # get privileges
    #     if "authorized-privileges" in scUser:
    #         scPrivs = scUser["authorized-privileges"]
    #         strPrivs = "<td>"
    #         for i in scPrivs:
    #             strPrivs += i["title"] + ", including the following functions: <br/>"
    #             scFunctions = i["functions-performed"]
    #             for x in scFunctions:
    #                 strPrivs += "- " + x + "<br/>"
    #         strPrivs += "</td>"
    #     else:
    #         strPrivs = "<td></td>"
    #     userTable += strPrivs
    #     # close the row
    #     userTable += "</tr>"
    # # close the table
    # userTable += "</table><br/>"
    # ssp["Environment"] += userTable

    # process components
    scComps = imps["components"]

    # loop through the components
    for role in scComps:
        component_status, created = status.objects.get_or_create(state=scComps[role]["status"]["state"])
        c, created = system_component.objects.get_or_create(
            uuid=role,
            title=scComps[role]["title"],
            desc=scComps[role]["description"],
            # todo fix component_status
            # component_status=component_status.id,
            component_type=scComps[role]["type"],
        )
        ssp.system_services.add(c.id)

        # process ports and protocols
        if "protocols" in scComps[role]:
            compPorts = scComps[role]["protocols"]
            for x in compPorts:
                p = protocol.objects.create(title=x["name"])
                ranges = x["port-ranges"]
                for pr in ranges:
                    z, created = port_range.objects.get_or_create(start=pr["start"], end=pr["end"], transport=pr["transport"])
                    p.portRanges.add(z.id)
                c.component_protocols.add(p.id)
        # process roles
        if "responsible-roles" in scComps[role]:
            system_component_roles = scComps["responsible-roles"]
            for system_component_role in system_component_roles:
                ur, created = user_role.objects.get_or_create(title=system_component_role)
                c.component_responsible_roles.add(ur.id)
    # TODO process inventory
    # if "system-inventory" in imps:
    #     scInvs = imps["system-inventory"]
    #     scItems = scInvs["inventory-items"]
    #     ssp["Environment"] += "<br/><h4>System Inventory</h4>"
    #     invTable = "<table border=\"1\" style=\"width: 100%;\"><tr style=\"font-weight: bold\"><td>ID</td><td>Description</td><td>Properties</td><td>Roles</td><td>Component</td></tr>"
    #     for i in scItems:
    #         # get the user
    #         userTable += "<tr>"
    #         scItem = scItems[i]
    #         invTable += "<td>" + scItem["asset-id"] + " (GUID: " + i + ")</td>"
    #         invTable += "<td>" + scItem["description"]
    #         if "remarks" in scItem:
    #             invTable += "<br/>" + scItem["remarks"]
    #         invTable += "</td>"
    #         # process properties and annotations
    #         invTable += "<td>"
    #         if "properties" in scItem:
    #             invProps = scItem["properties"]
    #             for x in invProps:
    #                 if "remarks" in x:
    #                     invTable += x["name"] + ": " + x["value"] + "(Remarks: " + x["remarks"] + ")<br/>"
    #                 else:
    #                     invTable += x["name"] + ": " + x["value"] + "<br/>"
    #             if "annotations" in scItem:
    #                 for x in scItem["annotations"]:
    #                     if "remarks" in x:
    #                         invTable += x["name"] + ": " + x["value"] + "(Remarks: " + x["remarks"] + ")<br/>"
    #                     else:
    #                         invTable += x["name"] + ": " + x["value"] + "<br/>"
    #         else:
    #             invTable += "N/A"
    #         invTable += "</td><td>"
    #         # process roles
    #         if "responsible-parties" in scItem:
    #             invRoles = scItem["responsible-parties"]
    #             for i in invRoles:
    #                 invTable += i + "<br/>"
    #         else:
    #             invTable += "N/A"
    #         invTable += "</td><td>"
    #         # process component
    #         if "implemented-components" in scItem:
    #             for z in scItem["implemented-components"]:
    #                 invTable += i + "<br/>"
    #             invTable += "</td>"
    #         else:
    #             invTable += "N/A</td>"
    #         # close the row
    #         invTable += "</tr>"
    #     # close the table
    #     invTable += "</table><br/>"
    #     ssp["Environment"] += invTable

    #############################################################################################
    # TODO: BACK MATTER SECTION
    #############################################################################################
    # if "back-matter" in level_1:
    #     back = level_1["back-matter"]
    #     resources = back["resources"]
    # for i in resources:
    #     resource
    #     if "uuid" in i:
    #         resourceTable += "<td>" + i["uuid"] + "</td>"
    #     else:
    #         resourceTable += "<td>N/A</td>"
    #     if "title" in i:
    #         if "desc" in i:
    #             resourceTable += "<td>" + i["title"] + " - " + i["desc"] + "</td>"
    #         else:
    #             resourceTable += "<td>" + i["title"] + "</td>"
    #     elif "desc" in i:
    #         resourceTable += "<td>" + i["desc"] + "</td>"
    #     else:
    #         resourceTable += "<td>N/A</td>"
    #     if "properties" in i:
    #         zProps = ""
    #         for z in i["properties"]:
    #             zProps += z["name"] + ": " + z["value"] + "<br/>"
    #         resourceTable += "<td>" + zProps + "</td>"
    #     else:
    #         resourceTable += "<td>N/A</td>"
    #     if "rlinks" in i:
    #         zLinks = ""
    #         for z in i["rlinks"]:
    #             zLinks += z["href"] + "<br/>"
    #         resourceTable += "<td>" + zLinks + "</td>"
    #     else:
    #         resourceTable += "<td>N/A</td>"
    #     # no data right now, commenting out
    #     # if "attachments" in i:
    #     #     zATT = ""
    #     #     for z in i["attachments"]:
    #     #         zATT += z["value"] + "<br/>"
    #     #     resourceTable += "<td>" + zATT + "</td>"
    #     # else:
    #     #     resourceTable += "<td>N/A</td>"
    #     if "remarks" in i:
    #         resourceTable += "<td>" + i["remarks"] + "</td>"
    #     else:
    #         resourceTable += "<td>N/A</td>"
    #     resourceTable += "</tr>"
    # resourceTable += "</table><br/>"
    # ssp["Description"] += resourceTable

    #############################################################################################
    # CONTROL IMPLEMENTATION
    #############################################################################################
    ctrlOBJ = level_1["control-implementation"]
    ctrls = ctrlOBJ["implemented-requirements"]

    # loop through the requirements
    for c in ctrls:
        nist_ctrl = nist_control.objects.get(control_id=c["control-id"])
        # assign the parent control
        sc, created = system_control.objects.get_or_create(nist_control_id=nist_ctrl.id, uuid=c["uuid"],control_primary_system_id=ssp.id)
        ssp.system_control_set.add(sc.id)
        # process statements
        if "statements" in c:
            ciState = c["statements"]
            for x in ciState:
                st = ciState[x]
                s, created = control_statement.objects.get_or_create(uuid=st["uuid"])
                if "remarks" in st:
                    s.remarks = st["remarks"]
                if "links" in st:
                    ciLinks = st["links"]
                    for z in ciLinks:
                        l, created = link.objects.get_or_create(text=z["text"], href=z["href"], rel=z["rel"])
                        s.links.add(l.id)
                if "by-components" in st:
                    ciComps = st["by-components"]
                    for z in ciComps:
                        component_id = ciComps[z]
                        s.text = system_component.objects.get(uuid=component_id)
                        s.text += ": "
                        s.text += z["description"]
