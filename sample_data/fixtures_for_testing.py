#!/usr/bin/env python


# This file has been automatically generated.
# Instead of changing it, create a file called import_helper.py
# and put there a class called ImportHelper(object) in it.
#
# This class will be specially casted so that instead of extending object,
# it will actually extend the class BasicImportHelper()
#
# That means you just have to overload the methods you want to
# change, leaving the other ones intact.
#
# Something that you might want to do is use transactions, for example.
#
# Also, don't forget to add the necessary Django imports.
#
# This file was generated with the following command:
# /Users/dan/code/opal/manage.py dumpscript catalog common component ctrl_profile ssp
#
# to restore it, run
# manage.py runscript module_name.this_script_name
#
# example: if manage.py is at ./manage.py
# and the script is at ./some_folder/some_script.py
# you must make sure ./some_folder/__init__.py exists
# and run  ./manage.py runscript some_folder.some_script
import os, sys
from uuid import UUID

from django.db import transaction

class BasicImportHelper:

    def pre_import(self):
        pass

    @transaction.atomic
    def run_import(self, import_data):
        import_data()

    def post_import(self):
        pass

    def locate_similar(self, current_object, search_data):
        # You will probably want to call this method from save_or_locate()
        # Example:
        #   new_obj = self.locate_similar(the_obj, {"national_id": the_obj.national_id } )

        the_obj = current_object.__class__.objects.get(**search_data)
        return the_obj

    def locate_object(self, original_class, original_pk_name, the_class, pk_name, pk_value, obj_content):
        # You may change this function to do specific lookup for specific objects
        #
        # original_class class of the django orm's object that needs to be located
        # original_pk_name the primary key of original_class
        # the_class      parent class of original_class which contains obj_content
        # pk_name        the primary key of original_class
        # pk_value       value of the primary_key
        # obj_content    content of the object which was not exported.
        #
        # You should use obj_content to locate the object on the target db
        #
        # An example where original_class and the_class are different is
        # when original_class is Farmer and the_class is Person. The table
        # may refer to a Farmer but you will actually need to locate Person
        # in order to instantiate that Farmer
        #
        # Example:
        #   if the_class == SurveyResultFormat or the_class == SurveyType or the_class == SurveyState:
        #       pk_name="name"
        #       pk_value=obj_content[pk_name]
        #   if the_class == StaffGroup:
        #       pk_value=8

        search_data = { pk_name: pk_value }
        the_obj = the_class.objects.get(**search_data)
        #print(the_obj)
        return the_obj


    def save_or_locate(self, the_obj):
        # Change this if you want to locate the object in the database
        try:
            the_obj.save()
        except:
            print("---------------")
            print("Error saving the following object:")
            print(the_obj.__class__)
            print(" ")
            print(the_obj.__dict__)
            print(" ")
            print(the_obj)
            print(" ")
            print("---------------")

            raise
        return the_obj


importer = None
try:
    import import_helper
    # We need this so ImportHelper can extend BasicImportHelper, although import_helper.py
    # has no knowlodge of this class
    importer = type("DynamicImportHelper", (import_helper.ImportHelper, BasicImportHelper ) , {} )()
except ImportError as e:
    # From Python 3.3 we can check e.name - string match is for backward compatibility.
    if 'import_helper' in str(e):
        importer = BasicImportHelper()
    else:
        raise

import datetime
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

try:
    import dateutil.parser
    from dateutil.tz import tzoffset
except ImportError:
    print("Please install python-dateutil")
    sys.exit(os.EX_USAGE)

def run():
    importer.pre_import()
    importer.run_import(import_data)
    importer.post_import()

def import_data():
    # Initial Imports

    # Processing model: catalog.models.available_catalog_list

    from catalog.models import available_catalog_list

    catalog_available_catalog_list_1 = available_catalog_list()
    catalog_available_catalog_list_1.uuid = UUID('4e2864a9-fc9d-406a-bc98-9aebb6e46682')
    catalog_available_catalog_list_1.created_at = dateutil.parser.parse("2023-02-28T15:40:45.829265+00:00")
    catalog_available_catalog_list_1.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.829285+00:00")
    catalog_available_catalog_list_1.remarks = ''
    catalog_available_catalog_list_1.catalog_uuid = UUID('fdac0321-959f-43ec-a91d-322da7d9761c')
    catalog_available_catalog_list_1.link = 'https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json'
    catalog_available_catalog_list_1.name = 'Electronic Version of NIST SP 800-53 Rev 5 Controls and SP 800-53A Rev 5 Assessment Procedures'
    catalog_available_catalog_list_1 = importer.save_or_locate(catalog_available_catalog_list_1)

    # Processing model: catalog.models.tests

    from catalog.models import tests


    # Processing model: catalog.models.constraints

    from catalog.models import constraints


    # Processing model: catalog.models.guidelines

    from catalog.models import guidelines


    # Processing model: common.models.port_ranges

    from common.models import port_ranges


    # Processing model: common.models.protocols

    from common.models import protocols


    # Processing model: common.models.props

    from common.models import props

    common_props_1 = props()
    common_props_1.uuid = UUID('6bc30ac9-3629-4d47-b6ea-3e2121f720eb')
    common_props_1.created_at = dateutil.parser.parse("2023-02-28T15:40:45.854005+00:00")
    common_props_1.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.854423+00:00")
    common_props_1.remarks = ''
    common_props_1.name = 'label'
    common_props_1.ns = 'https://csrc.nist.gov/ns/oscal'
    common_props_1.value = '1'
    common_props_1.property_class = ''
    common_props_1 = importer.save_or_locate(common_props_1)

    common_props_2 = props()
    common_props_2.uuid = UUID('b6e05b65-62a1-44be-adfc-6e6ffc44d2dc')
    common_props_2.created_at = dateutil.parser.parse("2023-02-28T15:40:45.856979+00:00")
    common_props_2.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.857325+00:00")
    common_props_2.remarks = ''
    common_props_2.name = 'label'
    common_props_2.ns = 'https://csrc.nist.gov/ns/oscal'
    common_props_2.value = '1.1'
    common_props_2.property_class = ''
    common_props_2 = importer.save_or_locate(common_props_2)

    common_props_3 = props()
    common_props_3.uuid = UUID('fed2ae8a-d5fc-4a10-ab5e-adbf58928a95')
    common_props_3.created_at = dateutil.parser.parse("2023-02-28T15:40:45.869700+00:00")
    common_props_3.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.870028+00:00")
    common_props_3.remarks = ''
    common_props_3.name = 'label'
    common_props_3.ns = 'https://csrc.nist.gov/ns/oscal'
    common_props_3.value = '1.1.1'
    common_props_3.property_class = ''
    common_props_3 = importer.save_or_locate(common_props_3)

    common_props_4 = props()
    common_props_4.uuid = UUID('2df22459-eb4d-483c-8cf5-f7dba1c1b02f')
    common_props_4.created_at = dateutil.parser.parse("2023-02-28T15:40:45.884934+00:00")
    common_props_4.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.885322+00:00")
    common_props_4.remarks = ''
    common_props_4.name = 'label'
    common_props_4.ns = 'https://csrc.nist.gov/ns/oscal'
    common_props_4.value = 'Other information'
    common_props_4.property_class = ''
    common_props_4 = importer.save_or_locate(common_props_4)

    common_props_5 = props()
    common_props_5.uuid = UUID('3ebbd83c-f994-4d70-a92e-efeb3d60574e')
    common_props_5.created_at = dateutil.parser.parse("2023-02-28T15:40:45.893857+00:00")
    common_props_5.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.894190+00:00")
    common_props_5.remarks = ''
    common_props_5.name = 'label'
    common_props_5.ns = 'https://csrc.nist.gov/ns/oscal'
    common_props_5.value = '1.1.2'
    common_props_5.property_class = ''
    common_props_5 = importer.save_or_locate(common_props_5)

    common_props_6 = props()
    common_props_6.uuid = UUID('05d5c8d5-03c2-4f84-b6c8-45c997eb039e')
    common_props_6.created_at = dateutil.parser.parse("2023-02-28T15:40:45.910838+00:00")
    common_props_6.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.911158+00:00")
    common_props_6.remarks = ''
    common_props_6.name = 'label'
    common_props_6.ns = 'https://csrc.nist.gov/ns/oscal'
    common_props_6.value = '2'
    common_props_6.property_class = ''
    common_props_6 = importer.save_or_locate(common_props_6)

    common_props_7 = props()
    common_props_7.uuid = UUID('24ca03c2-d230-43a5-93c8-2efaadc490bf')
    common_props_7.created_at = dateutil.parser.parse("2023-02-28T15:40:45.913329+00:00")
    common_props_7.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.913641+00:00")
    common_props_7.remarks = ''
    common_props_7.name = 'label'
    common_props_7.ns = 'https://csrc.nist.gov/ns/oscal'
    common_props_7.value = '2.1'
    common_props_7.property_class = ''
    common_props_7 = importer.save_or_locate(common_props_7)

    common_props_8 = props()
    common_props_8.uuid = UUID('dee43bee-86d9-48b0-bc46-4fb56728c9b2')
    common_props_8.created_at = dateutil.parser.parse("2023-02-28T15:40:45.918031+00:00")
    common_props_8.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.918388+00:00")
    common_props_8.remarks = ''
    common_props_8.name = 'label'
    common_props_8.ns = 'https://csrc.nist.gov/ns/oscal'
    common_props_8.value = '2.1.1'
    common_props_8.property_class = ''
    common_props_8 = importer.save_or_locate(common_props_8)

    common_props_9 = props()
    common_props_9.uuid = UUID('0c9cc702-b229-4928-a5c7-90ea33fd976b')
    common_props_9.created_at = dateutil.parser.parse("2023-02-28T15:40:45.942542+00:00")
    common_props_9.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.942877+00:00")
    common_props_9.remarks = ''
    common_props_9.name = 'label'
    common_props_9.ns = 'https://csrc.nist.gov/ns/oscal'
    common_props_9.value = '2.1.2'
    common_props_9.property_class = ''
    common_props_9 = importer.save_or_locate(common_props_9)

    common_props_10 = props()
    common_props_10.uuid = UUID('b38b4d39-ee4d-433d-9981-f08fdbfaad50')
    common_props_10.created_at = dateutil.parser.parse("2023-02-28T15:48:24.768252+00:00")
    common_props_10.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.768902+00:00")
    common_props_10.remarks = ''
    common_props_10.name = 'deployment-model'
    common_props_10.ns = 'https://csrc.nist.gov/ns/oscal'
    common_props_10.value = 'private'
    common_props_10.property_class = ''
    common_props_10 = importer.save_or_locate(common_props_10)

    common_props_11 = props()
    common_props_11.uuid = UUID('739b8dfe-ed65-4eb6-9cfb-f7a3c1579a3d')
    common_props_11.created_at = dateutil.parser.parse("2023-02-28T15:48:24.771332+00:00")
    common_props_11.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.771841+00:00")
    common_props_11.remarks = ''
    common_props_11.name = 'service-models'
    common_props_11.ns = 'https://csrc.nist.gov/ns/oscal'
    common_props_11.value = 'iaas'
    common_props_11.property_class = ''
    common_props_11 = importer.save_or_locate(common_props_11)

    common_props_12 = props()
    common_props_12.uuid = UUID('6f2fd4f5-50b8-43ca-9959-5ade4b9def0f')
    common_props_12.created_at = dateutil.parser.parse("2023-02-28T15:48:24.788353+00:00")
    common_props_12.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.788732+00:00")
    common_props_12.remarks = ''
    common_props_12.name = 'type'
    common_props_12.ns = 'https://csrc.nist.gov/ns/oscal'
    common_props_12.value = 'internal'
    common_props_12.property_class = ''
    common_props_12 = importer.save_or_locate(common_props_12)

    common_props_13 = props()
    common_props_13.uuid = UUID('d1674850-fc05-4b78-b2d5-4d03a9c9f51b')
    common_props_13.created_at = dateutil.parser.parse("2023-02-28T15:48:24.819769+00:00")
    common_props_13.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.820101+00:00")
    common_props_13.remarks = ''
    common_props_13.name = 'version'
    common_props_13.ns = 'https://csrc.nist.gov/ns/oscal'
    common_props_13.value = '2.1'
    common_props_13.property_class = ''
    common_props_13 = importer.save_or_locate(common_props_13)

    common_props_14 = props()
    common_props_14.uuid = UUID('00539e50-88ff-4a6e-a442-1fb6b21c2d21')
    common_props_14.created_at = dateutil.parser.parse("2023-02-28T15:48:24.821726+00:00")
    common_props_14.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.822061+00:00")
    common_props_14.remarks = ''
    common_props_14.name = 'last-modified-date'
    common_props_14.ns = 'https://csrc.nist.gov/ns/oscal'
    common_props_14.value = '20181015'
    common_props_14.property_class = ''
    common_props_14 = importer.save_or_locate(common_props_14)

    common_props_15 = props()
    common_props_15.uuid = UUID('d2139f90-5ddf-4933-ba9b-99a17a07b667')
    common_props_15.created_at = dateutil.parser.parse("2023-02-28T15:48:24.848987+00:00")
    common_props_15.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.849333+00:00")
    common_props_15.remarks = ''
    common_props_15.name = 'asset-id'
    common_props_15.ns = 'https://csrc.nist.gov/ns/oscal'
    common_props_15.value = 'asset-id-logging-server'
    common_props_15.property_class = ''
    common_props_15 = importer.save_or_locate(common_props_15)

    # Processing model: common.models.links

    from common.models import links

    common_links_1 = links()
    common_links_1.uuid = UUID('63bb26c0-a86a-428e-94be-04506679fca6')
    common_links_1.created_at = dateutil.parser.parse("2023-02-28T15:48:24.828156+00:00")
    common_links_1.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.828163+00:00")
    common_links_1.remarks = ''
    common_links_1.href = '#795533ab-9427-4abe-820f-0b571bacfe6d'
    common_links_1.rel = 'implements-policy'
    common_links_1.media_type = ''
    common_links_1.text = 'Ensures logs from components in new system are able to published to the logging server. Ensures log monitoring capabilities recognize new system as authorized.'
    common_links_1 = importer.save_or_locate(common_links_1)

    common_links_2 = links()
    common_links_2.uuid = UUID('95da9d0d-2622-4d8c-b1f4-15bee9d3ba71')
    common_links_2.created_at = dateutil.parser.parse("2023-02-28T15:48:24.836207+00:00")
    common_links_2.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.836214+00:00")
    common_links_2.remarks = ''
    common_links_2.href = '#795533ab-9427-4abe-820f-0b571bacfe6d'
    common_links_2.rel = 'implements-policy'
    common_links_2.media_type = ''
    common_links_2.text = 'Ensures that all host are known and authorized. Ensures that these hosts publish log events to the logging server.'
    common_links_2 = importer.save_or_locate(common_links_2)

    common_links_3 = links()
    common_links_3.uuid = UUID('7331f8f7-7df8-46d6-9778-f1ae86ca71a4')
    common_links_3.created_at = dateutil.parser.parse("2023-02-28T15:48:24.842334+00:00")
    common_links_3.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.842341+00:00")
    common_links_3.remarks = ''
    common_links_3.href = '#795533ab-9427-4abe-820f-0b571bacfe6d'
    common_links_3.rel = 'implements-policy'
    common_links_3.media_type = ''
    common_links_3.text = 'Ensures that all host are configured to publish log events to the logging server.'
    common_links_3 = importer.save_or_locate(common_links_3)

    # Processing model: common.models.revisions

    from common.models import revisions


    # Processing model: common.models.document_ids

    from common.models import document_ids


    # Processing model: common.models.roles

    from common.models import roles

    common_roles_1 = roles()
    common_roles_1.uuid = UUID('863344e8-374b-47f0-a91c-151387426b1f')
    common_roles_1.created_at = dateutil.parser.parse("2023-02-28T15:40:45.834806+00:00")
    common_roles_1.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.834822+00:00")
    common_roles_1.remarks = ''
    common_roles_1.role_id = 'AO'
    common_roles_1.title = 'Authorizing Official'
    common_roles_1.short_name = 'AO'
    common_roles_1.description = 'The authorizing official is a senior official or executive with the authority to formally assume responsibility and accountability for operating a system; providing common controls inherited by organizational systems; or using a system, service, or application from an external provider. The authorizing official is the only organizational official who can accept the security and privacy risk to organizational operations, organizational assets, and individuals.115 Authorizing officials typically have budgetary oversight for the system or are responsible for the mission and/or business operations supported by the system. Accordingly, authorizing officials are in management positions with a level of authority commensurate with understanding and accepting such security and privacy risks. Authorizing officials approve plans, memorandums of agreement or understanding, plans of action and milestones, and determine whether significant changes in the information systems or environments of operation require reauthorization.\\r\\nAuthorizing officials coordinate their activities with common control providers, system owners, chief information officers, senior agency information security officers, senior agency officials for privacy, system security and privacy officers, control assessors, senior accountable officials for risk management/risk executive (function), and other interested parties during the authorization process. With the increasing complexity of the mission/business processes in an organization, partnership arrangements, and the use of shared services, it is possible that a system may involve co-authorizing officials. If so, agreements are established between the co-authorizing officials and documented in the security and privacy plans. Authorizing officials are responsible and accountable for ensuring that authorization activities and functions that are delegated to authorizing official designated representatives are carried out as specified. For federal agencies, the role of authorizing official is an inherent U.S. Government function and is assigned to government personnel only.'
    common_roles_1 = importer.save_or_locate(common_roles_1)

    common_roles_2 = roles()
    common_roles_2.uuid = UUID('8dd9513c-d042-4aed-9084-0dfcc2ae74ca')
    common_roles_2.created_at = dateutil.parser.parse("2023-02-28T15:40:45.835743+00:00")
    common_roles_2.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.835752+00:00")
    common_roles_2.remarks = ''
    common_roles_2.role_id = 'AODR'
    common_roles_2.title = 'Authorizing Official Designated Representative'
    common_roles_2.short_name = 'AODR'
    common_roles_2.description = 'The authorizing official designated representative is an organizational official designated by the authorizing official who is empowered to act on behalf of the authorizing official to coordinate and conduct the day-to-day activities associated with managing risk to information systems and organizations. This includes carrying out many of the activities related to the execution of the RMF. The only activity that cannot be delegated by the authorizing official to the designated representative is the authorization decision and signing of the associated authorization decision document (i.e., the acceptance of risk).'
    common_roles_2 = importer.save_or_locate(common_roles_2)

    common_roles_3 = roles()
    common_roles_3.uuid = UUID('e32c1fe4-6245-4e06-90d1-cdb4e011ff01')
    common_roles_3.created_at = dateutil.parser.parse("2023-02-28T15:40:45.836453+00:00")
    common_roles_3.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.836462+00:00")
    common_roles_3.remarks = ''
    common_roles_3.role_id = 'CAO'
    common_roles_3.title = 'Chief Acquisition Officer'
    common_roles_3.short_name = 'CAO'
    common_roles_3.description = 'The chief acquisition officer is an organizational official designated by the head of an agency to advise and assist the head of agency and other agency officials to ensure that the mission of the agency is achieved through the management of the agency\\u2019s acquisition activities. The chief acquisition officer monitors the performance of acquisition activities and programs; establishes clear lines of authority, accountability, and responsibility for acquisition decision making within the agency; manages the direction and implementation of acquisition policy for the agency; and establishes policies, procedures, and practices that promote full and open competition from responsible sources to fulfill best value requirements considering the nature of the property or service procured. The Chief Acquisition Officer coordinates with mission or business owners, authorizing officials, senior accountable official for risk management, system owners, common control providers, senior agency information security officer, senior agency official for privacy, and risk executive (function) to ensure that security and privacy requirements are defined in organizational procurements and acquisitions.'
    common_roles_3 = importer.save_or_locate(common_roles_3)

    common_roles_4 = roles()
    common_roles_4.uuid = UUID('3f587b18-d85a-467c-82f8-55f378bcabf2')
    common_roles_4.created_at = dateutil.parser.parse("2023-02-28T15:40:45.837174+00:00")
    common_roles_4.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.837182+00:00")
    common_roles_4.remarks = ''
    common_roles_4.role_id = 'CIO'
    common_roles_4.title = 'Chief Information Officer'
    common_roles_4.short_name = 'CIO'
    common_roles_4.description = 'The chief information officer is an organizational official responsible for designating a senior agency information security officer; developing and maintaining security policies, procedures, and control techniques to address security requirements; overseeing personnel with significant responsibilities for security and ensuring that the personnel are adequately trained; assisting senior organizational officials concerning their security responsibilities; and reporting to the head of the agency on the effectiveness of the organization\\u2019s security program, including progress of remedial actions. The chief information officer, with the support of the senior accountable official for risk management, the risk executive (function), and the senior agency information security officer, works closely with authorizing officials and their designated representatives to help ensure that:\\r\\n\\u2022 An organization-wide security program is effectively implemented resulting in adequate security for all organizational systems and environments of operation;\\r\\n\\u2022 Security and privacy (including supply chain) risk management considerations are integrated into programming/planning/budgeting cycles, enterprise architectures, the SDLC, and acquisitions;\\r\\n\\u2022 Organizational systems and common controls are covered by approved system security plans and possess current authorizations;\\r\\n\\u2022 Security activities required across the organization are accomplished in an efficient, cost- effective, and timely manner; and\\r\\n\\u2022 There is centralized reporting of security activities.\\r\\nThe chief information officer and authorizing officials determine the allocation of resources dedicated to the protection of systems supporting the organization\\u2019s missions and business functions based on organizational priorities. For information systems that process personally identifiable information, the chief information officer and authorizing officials coordinate any determination about the allocation of resources dedicated to the protection of those systems with the senior agency official for privacy. For selected systems, the chief information officer may be designated as an authorizing official or a co-authorizing official with other senior organizational officials. The role of chief information officer is an inherent U.S. Government function and is assigned to government personnel only.'
    common_roles_4 = importer.save_or_locate(common_roles_4)

    common_roles_5 = roles()
    common_roles_5.uuid = UUID('00e8ce86-9034-4557-ae3d-ef4bbc0256c6')
    common_roles_5.created_at = dateutil.parser.parse("2023-02-28T15:40:45.837885+00:00")
    common_roles_5.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.837893+00:00")
    common_roles_5.remarks = ''
    common_roles_5.role_id = 'CA'
    common_roles_5.title = 'Control Assessor'
    common_roles_5.short_name = 'CA'
    common_roles_5.description = 'The control assessor is an individual, group, or organization responsible for conducting a comprehensive assessment of implemented controls and control enhancements to determine the effectiveness of the controls (i.e., the extent to which the controls are implemented correctly, operating as intended, and producing the desired outcome with respect to meeting the security and privacy requirements for the system and the organization). For systems, implemented system-specific controls and system-implemented parts of hybrid controls are assessed. For common controls, implemented common controls and common control- implemented parts of hybrid controls are assessed. The system owner and common control provider rely on the security and privacy expertise and judgment of the assessor to assess the implemented controls using the assessment procedures specified in the security and privacy assessment plans. Multiple control assessors who are differentiated by their expertise in specific control requirements or technologies may be required to conduct the assessment effectively. Prior to initiating the control assessment, assessors review the security and privacy plans to facilitate development of the assessment plans. Control assessors provide an assessment of the severity of the deficiencies discovered in the system, environment of operation, and common controls and can recommend corrective actions to address the identified vulnerabilities. For system-level control assessments, control assessors do not assess inherited controls, and only assess the system-implemented portions of hybrid controls. Control assessors prepare security and privacy assessment reports containing the results and findings from the assessment.\\r\\nThe required level of assessor independence is determined by the authorizing official based on laws, executive orders, directives, regulations, policies, standards, or guidelines. When a control assessment is conducted in support of an authorization decision or ongoing authorization, the authorizing official makes an explicit determination of the degree of independence required. Assessor independence is a factor in preserving an impartial and unbiased assessment process; determining the credibility of the assessment results; and ensuring that the authorizing official receives objective information to make an informed, risk-based authorization decision.\\r\\nThe senior agency official for privacy is responsible for assessing privacy controls and for providing privacy information to the authorizing official. At the discretion of the organization, privacy controls may be assessed by an independent assessor. However, in all cases, the senior agency official for privacy retains responsibility and accountability for the privacy program of the organization, including any privacy functions performed by the independent assessors.'
    common_roles_5 = importer.save_or_locate(common_roles_5)

    common_roles_6 = roles()
    common_roles_6.uuid = UUID('366212c4-340a-4c96-947f-0242801db8b6')
    common_roles_6.created_at = dateutil.parser.parse("2023-02-28T15:40:45.838577+00:00")
    common_roles_6.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.838585+00:00")
    common_roles_6.remarks = ''
    common_roles_6.role_id = 'EA'
    common_roles_6.title = 'Enterprise Architect'
    common_roles_6.short_name = 'EA'
    common_roles_6.description = "The enterprise architect is an individual or group responsible for working with the leadership and subject matter experts in an organization to build a holistic view of the organization's missions and business functions, mission/business processes, information, and information technology assets. With respect to information security and privacy, enterprise architects:\\r\\n\\u2022 Implement an enterprise architecture strategy that facilitates effective security and privacy solutions;\\r\\n\\u2022 Coordinate with security and privacy architects to determine the optimal placement of systems/system elements within the enterprise architecture and to address security and privacy issues between systems and the enterprise architecture;\\r\\n\\u2022 Assist in reducing complexity within the IT infrastructure to facilitate security;\\r\\n\\u2022 Assist with determining appropriate control implementations and initial configuration\\r\\nbaselines as they relate to the enterprise architecture;\\r\\n\\u2022 Collaborate with system owners and authorizing officials to facilitate authorization boundary determinations and allocation of controls to system elements;\\r\\n\\u2022 Serve as part of the Risk Executive (function); and\\r\\n\\u2022 Assist with integration of the organizational risk management strategy and system-level security and privacy requirements into program, planning, and budgeting activities, the SDLC, acquisition processes, security and privacy (including supply chain) risk management, and systems engineering processes."
    common_roles_6 = importer.save_or_locate(common_roles_6)

    common_roles_7 = roles()
    common_roles_7.uuid = UUID('5ff651c3-98a0-4bd9-b2f6-8174a860fac4')
    common_roles_7.created_at = dateutil.parser.parse("2023-02-28T15:40:45.839252+00:00")
    common_roles_7.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.839259+00:00")
    common_roles_7.remarks = ''
    common_roles_7.role_id = 'HOA'
    common_roles_7.title = 'Head Of Agency'
    common_roles_7.short_name = 'HOA'
    common_roles_7.description = 'The head of agency is responsible and accountable for providing information security protections commensurate with the risk to organizational operations and assets, individuals, other organizations, and the Nation\\u2014that is, risk resulting from unauthorized access, use, disclosure, disruption, modification, or destruction of information collected or maintained by or on behalf of the agency; and the information systems used or operated by an agency or by a contractor of an agency or other organization on behalf of an agency. The head of agency is also the senior official in an organization with the responsibility for ensuring that privacy interests are protected and that PII is managed responsibly within the organization. The heads of agencies ensure that:\\r\\n\\u2022 Information security and privacy management processes are integrated with strategic and operational planning processes;\\r\\n\\u2022 Senior officials within the organization provide information security for the information and systems supporting the operations and assets under their control;\\r\\n\\u2022 Senior agency officials for privacy are designated who are responsible and accountable for ensuring compliance with applicable privacy requirements, managing privacy risk, and the organization\\u2019s privacy program; and\\r\\n\\u2022 The organization has adequately trained personnel to assist in complying with security and privacy requirements in legislation, executive orders, policies, directives, instructions, standards, and guidelines.\\r\\nThe head of agency establishes the organizational commitment and the actions required to effectively manage security and privacy risk and protect the missions and business functions being carried out by the organization. The head of agency establishes security and privacy accountability and provides active support and oversight of monitoring and improvement for the security and privacy programs. Senior leadership commitment to security and privacy establishes a level of due diligence within the organization that promotes a climate for mission and business success.'
    common_roles_7 = importer.save_or_locate(common_roles_7)

    common_roles_8 = roles()
    common_roles_8.uuid = UUID('59ef708c-02d6-4b4c-920b-eaae39c9e67a')
    common_roles_8.created_at = dateutil.parser.parse("2023-02-28T15:40:45.839942+00:00")
    common_roles_8.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.839950+00:00")
    common_roles_8.remarks = ''
    common_roles_8.role_id = 'IO'
    common_roles_8.title = 'Information Owner'
    common_roles_8.short_name = 'IO'
    common_roles_8.description = 'The information owner or steward is an organizational official with statutory, management, or operational authority for specified information and the responsibility for establishing the policies and procedures governing its generation, collection, processing, dissemination, and disposal. In information-sharing environments, the information owner/steward is responsible for establishing the rules for appropriate use and protection of the information and retains that responsibility even when the information is shared with or provided to other organizations. The owner/steward of the information processed, stored, or transmitted by a system may or may not be the same individual as the system owner. An individual system may contain information from multiple information owners/stewards. Information owners/stewards provide input to system owners regarding the security and privacy requirements and controls for the systems where the information is processed, stored, or transmitted.'
    common_roles_8 = importer.save_or_locate(common_roles_8)

    common_roles_9 = roles()
    common_roles_9.uuid = UUID('0e3742e2-5791-4cce-8c03-1e2809715ae5')
    common_roles_9.created_at = dateutil.parser.parse("2023-02-28T15:40:45.840631+00:00")
    common_roles_9.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.840638+00:00")
    common_roles_9.remarks = ''
    common_roles_9.role_id = 'MO'
    common_roles_9.title = 'Mission Owner'
    common_roles_9.short_name = 'MO'
    common_roles_9.description = 'The mission or business owner is the senior official or executive within an organization with specific mission or line of business responsibilities and that has a security or privacy interest in the organizational systems supporting those missions or lines of business. Mission or business owners are key stakeholders that have a significant role in establishing organizational mission and business processes and the protection needs and security and privacy requirements that ensure the successful conduct of the organization\\u2019s missions and business operations. Mission and business owners provide essential inputs to the risk management strategy, play an active part in the SDLC, and may also serve in the role of authorizing official.'
    common_roles_9 = importer.save_or_locate(common_roles_9)

    common_roles_10 = roles()
    common_roles_10.uuid = UUID('9943797e-3eec-4503-a125-27ed871f783a')
    common_roles_10.created_at = dateutil.parser.parse("2023-02-28T15:40:45.841292+00:00")
    common_roles_10.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.841300+00:00")
    common_roles_10.remarks = ''
    common_roles_10.role_id = 'SAORM'
    common_roles_10.title = 'Senior Accountable Official For Risk Management'
    common_roles_10.short_name = 'SAORM'
    common_roles_10.description = 'The senior accountable official for risk management is the individual that leads and manages the risk executive (function) in an organization and is responsible for aligning information security and privacy risk management processes with strategic, operational, and budgetary planning processes. The senior accountable official for risk management is the head of the agency or an individual designated by the head of the agency. The senior accountable official for risk management determines the organizational structure and responsibilities of the risk executive (function), and in coordination with the head of the agency, may retain the risk executive (function) or delegate the function to another organizational official or group. The senior accountable official for risk management is an inherent U.S. Government function and is assigned to government personnel only.'
    common_roles_10 = importer.save_or_locate(common_roles_10)

    common_roles_11 = roles()
    common_roles_11.uuid = UUID('1df3f304-1668-4685-919f-af7cfa75568a')
    common_roles_11.created_at = dateutil.parser.parse("2023-02-28T15:40:45.841965+00:00")
    common_roles_11.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.841973+00:00")
    common_roles_11.remarks = ''
    common_roles_11.role_id = 'CISO'
    common_roles_11.title = 'Senior Agency Information Security Officer'
    common_roles_11.short_name = 'CISO'
    common_roles_11.description = 'The senior agency information security officer is an organizational official responsible for carrying out the chief information officer security responsibilities under FISMA, and serving as the primary liaison for the chief information officer to the organization\\u2019s authorizing officials, system owners, common control providers, and system security officers. The senior agency information security officer is also responsible for coordinating with the senior agency official for privacy to ensure coordination between privacy and information security programs. The senior agency information security officer possesses the professional qualifications, including training and experience, required to administer security program functions; maintains security duties as a primary responsibility; and heads an office with the specific mission and resources to assist the organization in achieving trustworthy, secure information and systems in accordance with the requirements in FISMA. The senior agency information security officer may serve as authorizing official designated representative or as a security control assessor. The role of senior agency information security officer is an inherent U.S. Government function and is therefore assigned to government personnel only. Organizations may also refer to the senior agency information security officer as the senior information security officer or chief information security officer.'
    common_roles_11 = importer.save_or_locate(common_roles_11)

    common_roles_12 = roles()
    common_roles_12.uuid = UUID('9b27d82b-f133-4d97-822a-35ebfccc0d5b')
    common_roles_12.created_at = dateutil.parser.parse("2023-02-28T15:40:45.842620+00:00")
    common_roles_12.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.842627+00:00")
    common_roles_12.remarks = ''
    common_roles_12.role_id = 'SAOP'
    common_roles_12.title = 'Senior Agency Official For Privacy'
    common_roles_12.short_name = 'SAOP'
    common_roles_12.description = 'The senior agency official for privacy is the senior official or executive with agency-wide responsibility and accountability for ensuring compliance with applicable privacy requirements and managing privacy risk. Among other things, the senior agency official for privacy is responsible for:\\r\\n\\u2022 Coordinating with the senior agency information security officer to ensure coordination of privacy and information security activities;\\r\\n\\u2022 Reviewing and approving the categorization of information systems that create, collect, use, process, store, maintain, disseminate, disclose, or dispose of personally identifiable information;\\r\\n\\u2022 Designating which privacy controls will be treated as program management, common, system-specific, and hybrid privacy controls;\\r\\n\\u2022 Identifying assessment methodologies and metrics to determine whether privacy controls are implemented correctly, operating as intended, and sufficient to ensure compliance with applicable privacy requirements and manage privacy risks;\\r\\n\\u2022 Reviewing and approving privacy plans for information systems prior to authorization, reauthorization, or ongoing authorization;\\r\\n\\u2022 Reviewing authorization packages for information systems that create, collect, use, process, store, maintain, disseminate, disclose, or dispose of personally identifiable information to ensure compliance with privacy requirements and manage privacy risks;\\r\\n\\u2022 Conducting and documenting the results of privacy control assessments to verify the continued effectiveness of all privacy controls selected and implemented at the agency; and\\r\\n\\u2022 Establishing and maintaining a privacy continuous monitoring program to maintain ongoing awareness of privacy risks and assess privacy controls at a frequency sufficient to ensure compliance with privacy requirements and manage privacy risks.\\r\\nThe role of senior agency official for privacy is an inherent U.S. Government function and is therefore assigned to government personnel only.'
    common_roles_12 = importer.save_or_locate(common_roles_12)

    common_roles_13 = roles()
    common_roles_13.uuid = UUID('e14e8304-4f03-49b1-b272-718cb805fe67')
    common_roles_13.created_at = dateutil.parser.parse("2023-02-28T15:40:45.843286+00:00")
    common_roles_13.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.843294+00:00")
    common_roles_13.remarks = ''
    common_roles_13.role_id = 'SA'
    common_roles_13.title = 'System Administrator'
    common_roles_13.short_name = 'SA'
    common_roles_13.description = 'The system administrator is an individual, group, or organization responsible for setting up and maintaining a system or specific system elements. System administrator responsibilities include, for example, installing, configuring, and updating hardware and software; establishing and managing user accounts; overseeing or conducting backup, recovery, and reconstitution activities; implementing controls; and adhering to and enforcing organizational security and privacy policies and procedures. The system administrator role includes other types of system administrators (e.g., database administrators, network administrators, web administrators, and application administrators).'
    common_roles_13 = importer.save_or_locate(common_roles_13)

    common_roles_14 = roles()
    common_roles_14.uuid = UUID('e9bb1c22-2c37-4c01-956b-803a5be2a45a')
    common_roles_14.created_at = dateutil.parser.parse("2023-02-28T15:40:45.843953+00:00")
    common_roles_14.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.843961+00:00")
    common_roles_14.remarks = ''
    common_roles_14.role_id = 'SO'
    common_roles_14.title = 'System Owner'
    common_roles_14.short_name = 'SO'
    common_roles_14.description = 'The system owner is an organizational official responsible for the procurement, development, integration, modification, operation, maintenance, and disposal of a system.121 The system owner is responsible for addressing the operational interests of the user community (i.e., users who require access to the system to satisfy mission, business, or operational requirements) and for ensuring compliance with security requirements. In coordination with the system security and privacy officers, the system owner is responsible for the development and maintenance of the security and privacy plans and ensures that the system is operated in accordance with the selected and implemented controls.\\r\\nIn coordination with the information owner/steward, the system owner decides who has access to the system (and with what types of privileges or access rights).122 The system owner ensures that system users and support personnel receive the requisite security and privacy training. Based on guidance from the authorizing official, the system owner informs organizational officials of the need to conduct the authorization, ensures that resources are available for the effort, and provides the required system access, information, and documentation to control assessors. The system owner receives the security and privacy assessment results from the control assessors. After taking appropriate steps to reduce or eliminate vulnerabilities or security and privacy risks, the system owner assembles the authorization package and submits the package to the authorizing official or the authorizing official designated representative for adjudication.'
    common_roles_14 = importer.save_or_locate(common_roles_14)

    common_roles_15 = roles()
    common_roles_15.uuid = UUID('534b4f5d-5e54-48a9-af5b-23a9e50aa27d')
    common_roles_15.created_at = dateutil.parser.parse("2023-02-28T15:40:45.844619+00:00")
    common_roles_15.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.844626+00:00")
    common_roles_15.remarks = ''
    common_roles_15.role_id = 'SSO'
    common_roles_15.title = 'System Security Officer'
    common_roles_15.short_name = 'SSO'
    common_roles_15.description = 'The system security or privacy officer124 is an individual responsible for ensuring that the security and privacy posture is maintained for an organizational system and works in close collaboration with the system owner. The system security or privacy officer also serves as a principal advisor on all matters, technical and otherwise, involving the controls for the system. The system security or privacy officer has the knowledge and expertise to manage the security or privacy aspects of an organizational system and, in many organizations, is assigned responsibility for the day-to-day system security or privacy operations. This responsibility may also include, but is not limited to, physical and environmental protection; personnel security; incident handling; and security and privacy training and awareness.\\r\\nThe system security or privacy officer may be called on to assist in the development of the system-level security and privacy policies and procedures and to ensure compliance with those policies and procedures. In close coordination with the system owner, the system security or privacy officer often plays an active role in the monitoring of a system and its environment of operation to include developing and updating security and privacy plans, managing and controlling changes to the system, and assessing the security or privacy impact of those changes.\\r\\nWhen the system security officer and system privacy officer are separate roles, the system security officer is generally responsible for aspects of the system that protect information and information systems from unauthorized system activity or behavior to provide confidentiality, integrity, and availability. The system privacy officer is responsible for aspects of the system that ensure compliance with privacy requirements and manage the privacy risks to individuals associated with the processing of PII. The responsibilities of system security officers and system privacy officers overlap regarding aspects of the system that protect the security of PII.'
    common_roles_15 = importer.save_or_locate(common_roles_15)

    common_roles_16 = roles()
    common_roles_16.uuid = UUID('c0a76187-95d4-405f-acd0-5f7592a26b5f')
    common_roles_16.created_at = dateutil.parser.parse("2023-02-28T15:40:45.845374+00:00")
    common_roles_16.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.845385+00:00")
    common_roles_16.remarks = ''
    common_roles_16.role_id = 'SPO'
    common_roles_16.title = 'System Privacy Officer'
    common_roles_16.short_name = 'SPO'
    common_roles_16.description = 'The system security or privacy officer124 is an individual responsible for ensuring that the security and privacy posture is maintained for an organizational system and works in close collaboration with the system owner. The system security or privacy officer also serves as a principal advisor on all matters, technical and otherwise, involving the controls for the system. The system security or privacy officer has the knowledge and expertise to manage the security or privacy aspects of an organizational system and, in many organizations, is assigned responsibility for the day-to-day system security or privacy operations. This responsibility may also include, but is not limited to, physical and environmental protection; personnel security; incident handling; and security and privacy training and awareness.\\r\\nThe system security or privacy officer may be called on to assist in the development of the system-level security and privacy policies and procedures and to ensure compliance with those policies and procedures. In close coordination with the system owner, the system security or privacy officer often plays an active role in the monitoring of a system and its environment of operation to include developing and updating security and privacy plans, managing and controlling changes to the system, and assessing the security or privacy impact of those changes.\\r\\nWhen the system security officer and system privacy officer are separate roles, the system security officer is generally responsible for aspects of the system that protect information and information systems from unauthorized system activity or behavior to provide confidentiality, integrity, and availability. The system privacy officer is responsible for aspects of the system that ensure compliance with privacy requirements and manage the privacy risks to individuals associated with the processing of PII. The responsibilities of system security officers and system privacy officers overlap regarding aspects of the system that protect the security of PII.'
    common_roles_16 = importer.save_or_locate(common_roles_16)

    common_roles_17 = roles()
    common_roles_17.uuid = UUID('738f561d-1795-451a-9cb2-928dcdf3ce48')
    common_roles_17.created_at = dateutil.parser.parse("2023-02-28T15:40:45.846104+00:00")
    common_roles_17.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.846112+00:00")
    common_roles_17.remarks = ''
    common_roles_17.role_id = 'USER'
    common_roles_17.title = 'System User'
    common_roles_17.short_name = 'USER'
    common_roles_17.description = 'The system user is an individual or (system) process acting on behalf of an individual that is authorized to access information and information systems to perform assigned duties. System user responsibilities include, but are not limited to, adhering to organizational policies that govern acceptable use of organizational systems; using the organization-provided information technology resources for defined purposes only; and reporting anomalous or suspicious system behavior.'
    common_roles_17 = importer.save_or_locate(common_roles_17)

    common_roles_18 = roles()
    common_roles_18.uuid = UUID('cdfd40ae-2a9a-4920-9ae5-389bc3755e6b')
    common_roles_18.created_at = dateutil.parser.parse("2023-02-28T15:40:45.846749+00:00")
    common_roles_18.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.846756+00:00")
    common_roles_18.remarks = ''
    common_roles_18.role_id = 'SSE'
    common_roles_18.title = 'Systems Security Or Privacy Engineer'
    common_roles_18.short_name = 'SSE'
    common_roles_18.description = 'The systems security or privacy engineer is an individual, group, or organization responsible for conducting systems security or privacy engineering activities as part of the SDLC. Systems security and privacy engineering is a process that captures and refines security and privacy requirements for systems and ensures that the requirements are effectively integrated into systems and system elements through security or privacy architecting, design, development, and configuration. Systems security or privacy engineers are part of the development team\\u2014 designing and developing organizational systems or upgrading existing systems along with ensuring continuous monitoring requirements are addressed at the system level. Systems security or privacy engineers employ best practices when implementing controls including software engineering methodologies; system and security or privacy engineering principles; secure or privacy-enhancing design, secure or privacy-enhancing architecture, and secure or privacy-enhancing coding techniques. Systems security or privacy engineers coordinate security and privacy activities with senior agency information security officers, senior agency officials for privacy, security and privacy architects, system owners, common control providers, and system security or privacy officers.\\r\\nWhen the systems security engineer and privacy engineer are separate roles, the systems security engineer is generally responsible for those activities associated with protecting information and information systems from unauthorized system activity or behavior to provide confidentiality, integrity, and availability. The privacy engineer is responsible for those activities associated with ensuring compliance with privacy requirements and managing the privacy risks to individuals associated with the processing of PII. The responsibilities of systems security engineers and privacy engineers overlap regarding activities associated with protecting the security of PII.'
    common_roles_18 = importer.save_or_locate(common_roles_18)

    common_roles_19 = roles()
    common_roles_19.uuid = UUID('c96dd999-a30a-4232-9b6f-fdf0ec657bda')
    common_roles_19.created_at = dateutil.parser.parse("2023-02-28T15:48:24.792851+00:00")
    common_roles_19.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.792859+00:00")
    common_roles_19.remarks = ''
    common_roles_19.role_id = 'asset-administrator'
    common_roles_19.title = ''
    common_roles_19.short_name = ''
    common_roles_19.description = ''
    common_roles_19 = importer.save_or_locate(common_roles_19)

    common_roles_20 = roles()
    common_roles_20.uuid = UUID('ffd1b71f-de7e-4663-a670-d313b13b7f06')
    common_roles_20.created_at = dateutil.parser.parse("2023-02-28T15:48:24.799930+00:00")
    common_roles_20.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.799937+00:00")
    common_roles_20.remarks = ''
    common_roles_20.role_id = 'asset-owner'
    common_roles_20.title = ''
    common_roles_20.short_name = ''
    common_roles_20.description = ''
    common_roles_20 = importer.save_or_locate(common_roles_20)

    common_roles_21 = roles()
    common_roles_21.uuid = UUID('222bc534-a564-4174-bf66-089227f7a6f6')
    common_roles_21.created_at = dateutil.parser.parse("2023-02-28T15:48:24.804450+00:00")
    common_roles_21.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.804457+00:00")
    common_roles_21.remarks = ''
    common_roles_21.role_id = 'legal-officer'
    common_roles_21.title = ''
    common_roles_21.short_name = ''
    common_roles_21.description = ''
    common_roles_21 = importer.save_or_locate(common_roles_21)

    common_roles_22 = roles()
    common_roles_22.uuid = UUID('70f393e5-c7f3-4b18-b604-2df7224462f3')
    common_roles_22.created_at = dateutil.parser.parse("2023-02-28T15:48:24.809283+00:00")
    common_roles_22.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.809291+00:00")
    common_roles_22.remarks = ''
    common_roles_22.role_id = 'provider'
    common_roles_22.title = ''
    common_roles_22.short_name = ''
    common_roles_22.description = ''
    common_roles_22 = importer.save_or_locate(common_roles_22)

    # Processing model: common.models.emails

    from common.models import emails


    # Processing model: common.models.telephone_numbers

    from common.models import telephone_numbers


    # Processing model: common.models.addresses

    from common.models import addresses


    # Processing model: common.models.locations

    from common.models import locations


    # Processing model: common.models.external_ids

    from common.models import external_ids


    # Processing model: common.models.organizations

    from common.models import organizations


    # Processing model: common.models.parties

    from common.models import parties

    common_parties_1 = parties()
    common_parties_1.uuid = UUID('3b2a5599-cc37-403f-ae36-5708fa804b27')
    common_parties_1.created_at = dateutil.parser.parse("2023-02-28T15:48:24.735456+00:00")
    common_parties_1.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.736802+00:00")
    common_parties_1.remarks = ''
    common_parties_1.type = 'organization'
    common_parties_1.name = 'Enterprise Asset Owners'
    common_parties_1.short_name = ''
    common_parties_1.address = None
    common_parties_1 = importer.save_or_locate(common_parties_1)

    common_parties_2 = parties()
    common_parties_2.uuid = UUID('833ac398-5c9a-4e6b-acba-2a9c11399da0')
    common_parties_2.created_at = dateutil.parser.parse("2023-02-28T15:48:24.740051+00:00")
    common_parties_2.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.740851+00:00")
    common_parties_2.remarks = ''
    common_parties_2.type = 'organization'
    common_parties_2.name = 'Enterprise Asset Administrators'
    common_parties_2.short_name = ''
    common_parties_2.address = None
    common_parties_2 = importer.save_or_locate(common_parties_2)

    common_parties_3 = parties()
    common_parties_3.uuid = UUID('ec485dcf-2519-43f5-8e7d-014cc315332d')
    common_parties_3.created_at = dateutil.parser.parse("2023-02-28T15:48:24.743494+00:00")
    common_parties_3.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.744148+00:00")
    common_parties_3.remarks = ''
    common_parties_3.type = 'organization'
    common_parties_3.name = 'Legal Department'
    common_parties_3.short_name = ''
    common_parties_3.address = None
    common_parties_3 = importer.save_or_locate(common_parties_3)

    common_parties_4 = parties()
    common_parties_4.uuid = UUID('0f0c15ed-565e-4ce9-8670-b54853d0bf03')
    common_parties_4.created_at = dateutil.parser.parse("2023-02-28T15:48:24.746525+00:00")
    common_parties_4.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.747256+00:00")
    common_parties_4.remarks = ''
    common_parties_4.type = 'organization'
    common_parties_4.name = 'IT Department'
    common_parties_4.short_name = ''
    common_parties_4.address = None
    common_parties_4 = importer.save_or_locate(common_parties_4)

    common_parties_5 = parties()
    common_parties_5.uuid = UUID('96c362ee-a012-4e07-92f3-486ab303b0e7')
    common_parties_5.created_at = dateutil.parser.parse("2023-02-28T15:48:24.750213+00:00")
    common_parties_5.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.750907+00:00")
    common_parties_5.remarks = ''
    common_parties_5.type = 'organization'
    common_parties_5.name = 'Acme Corp'
    common_parties_5.short_name = ''
    common_parties_5.address = None
    common_parties_5 = importer.save_or_locate(common_parties_5)

    common_parties_6 = parties()
    common_parties_6.uuid = UUID('f8d9b85b-0f13-40c2-9776-8df54d3f0738')
    common_parties_6.created_at = dateutil.parser.parse("2023-02-28T15:48:24.812216+00:00")
    common_parties_6.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.812575+00:00")
    common_parties_6.remarks = ''
    common_parties_6.type = ''
    common_parties_6.name = ''
    common_parties_6.short_name = ''
    common_parties_6.address = None
    common_parties_6 = importer.save_or_locate(common_parties_6)

    # Processing model: common.models.responsible_parties

    from common.models import responsible_parties

    common_responsible_parties_1 = responsible_parties()
    common_responsible_parties_1.uuid = UUID('9a6daab9-3df2-4d85-ae5f-48aca906a837')
    common_responsible_parties_1.created_at = dateutil.parser.parse("2023-02-28T15:48:24.851139+00:00")
    common_responsible_parties_1.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.851514+00:00")
    common_responsible_parties_1.role_id = ''
    common_responsible_parties_1 = importer.save_or_locate(common_responsible_parties_1)

    # Processing model: common.models.metadata

    from common.models import metadata

    common_metadata_1 = metadata()
    common_metadata_1.uuid = UUID('85013b6b-62ff-4b26-9bc9-7fe9d56b205c')
    common_metadata_1.created_at = dateutil.parser.parse("2023-02-28T15:40:45.850605+00:00")
    common_metadata_1.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.851282+00:00")
    common_metadata_1.remarks = 'The following is a short excerpt from [ISO/IEC 27002:2013](https://www.iso.org/standard/54533.html), *Information technology — Security techniques — Code of practice for information security controls*. This work is provided here under copyright "fair use" for non-profit, educational purposes only. Copyrights for this work are held by the publisher, the International Organization for Standardization (ISO).'
    common_metadata_1.title = 'Sample Security Catalog *for Demonstration* and Testing'
    common_metadata_1.published = dateutil.parser.parse("2020-02-02T15:01:04.736000+00:00")
    common_metadata_1.last_modified = dateutil.parser.parse("2021-06-08T17:57:28.355446+00:00")
    common_metadata_1.version = '1.0'
    common_metadata_1.oscal_version = '1.0.0'
    common_metadata_1 = importer.save_or_locate(common_metadata_1)

    common_metadata_2 = metadata()
    common_metadata_2.uuid = UUID('b6458608-bb7f-418c-9a31-9dfeb2a536d5')
    common_metadata_2.created_at = dateutil.parser.parse("2023-02-28T15:40:45.958768+00:00")
    common_metadata_2.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.958775+00:00")
    common_metadata_2.remarks = ''
    common_metadata_2.title = 'Sample Security Catalog *for Demonstration* and Testing'
    common_metadata_2.published = None
    common_metadata_2.last_modified = dateutil.parser.parse("2023-02-28T15:40:45.958726+00:00")
    common_metadata_2.version = '1.0'
    common_metadata_2.oscal_version = 'v1.0.3'
    common_metadata_2 = importer.save_or_locate(common_metadata_2)

    common_metadata_3 = metadata()
    common_metadata_3.uuid = UUID('095ecaa9-3c7b-4816-8fcb-937f13143f04')
    common_metadata_3.created_at = dateutil.parser.parse("2023-02-28T15:48:24.732584+00:00")
    common_metadata_3.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.753886+00:00")
    common_metadata_3.remarks = ''
    common_metadata_3.title = 'Enterprise Logging and Auditing System Security Plan'
    common_metadata_3.published = None
    common_metadata_3.last_modified = dateutil.parser.parse("2021-06-08T17:57:28.355446+00:00")
    common_metadata_3.version = '1.0'
    common_metadata_3.oscal_version = '1.0.0'
    common_metadata_3 = importer.save_or_locate(common_metadata_3)

    common_metadata_3.parties.add(common_parties_1)
    common_metadata_3.parties.add(common_parties_2)
    common_metadata_3.parties.add(common_parties_3)
    common_metadata_3.parties.add(common_parties_4)
    common_metadata_3.parties.add(common_parties_5)

    # Processing model: common.models.citations

    from common.models import citations


    # Processing model: common.models.hashes

    from common.models import hashes


    # Processing model: common.models.rlinks

    from common.models import rlinks


    # Processing model: common.models.base64

    from common.models import base64


    # Processing model: common.models.resources

    from common.models import resources


    # Processing model: common.models.back_matter

    from common.models import back_matter


    # Processing model: component.models.responsible_roles

    from component.models import responsible_roles

    component_responsible_roles_1 = responsible_roles()
    component_responsible_roles_1.uuid = UUID('c9786088-a20c-4a2a-9224-0f2aa5e7d64e')
    component_responsible_roles_1.created_at = dateutil.parser.parse("2023-02-28T15:48:24.809673+00:00")
    component_responsible_roles_1.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.814215+00:00")
    component_responsible_roles_1.remarks = ''
    component_responsible_roles_1.role_id = common_roles_22
    component_responsible_roles_1 = importer.save_or_locate(component_responsible_roles_1)

    component_responsible_roles_1.party_uuids.add(common_parties_6)

    # Processing model: component.models.provided_control_implementation

    from component.models import provided_control_implementation


    # Processing model: component.models.components

    from component.models import components

    component_components_1 = components()
    component_components_1.uuid = UUID('53bab1d4-cd25-4261-ba3e-d250b63d2556')
    component_components_1.created_at = dateutil.parser.parse("2023-02-28T15:40:45.983792+00:00")
    component_components_1.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.984186+00:00")
    component_components_1.remarks = ''
    component_components_1.type = 'policy'
    component_components_1.title = 'Access control Policy'
    component_components_1.description = 'This Component Policy was automatically created during the import of Sample Security Catalog *for Demonstration* and Testing'
    component_components_1.purpose = 'This Component Policy was automatically created during the import of Sample Security Catalog *for Demonstration* and Testing'
    component_components_1.status = 'under-development'
    component_components_1 = importer.save_or_locate(component_components_1)

    component_components_2 = components()
    component_components_2.uuid = UUID('4938767c-dd8b-4ea4-b74a-fafffd48ac99')
    component_components_2.created_at = dateutil.parser.parse("2023-02-28T15:48:24.840405+00:00")
    component_components_2.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.845144+00:00")
    component_components_2.remarks = ''
    component_components_2.type = 'guidance'
    component_components_2.title = 'Configuration Management Guidance'
    component_components_2.description = 'Describes how to configure a component to ensure its logs are transmitted to Splunk in the appropriate format. Also describes how to configure time synchronization.'
    component_components_2.purpose = ''
    component_components_2.status = ''
    component_components_2 = importer.save_or_locate(component_components_2)

    component_components_2.props.add(common_props_14)
    component_components_2.links.add(common_links_3)
    component_components_2.responsible_roles.add(component_responsible_roles_1)

    component_components_3 = components()
    component_components_3.uuid = UUID('795533ab-9427-4abe-820f-0b571bacfe6d')
    component_components_3.created_at = dateutil.parser.parse("2023-02-28T15:48:24.819183+00:00")
    component_components_3.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.824875+00:00")
    component_components_3.remarks = ''
    component_components_3.type = 'policy'
    component_components_3.title = 'Enterprise Logging, Monitoring, and Alerting Policy'
    component_components_3.description = 'Requires all components to send logs to the enterprise logging solution\n\n- Requires all components synchronize their time with the appropriate enterprise time service, and at what frequency.\n\n- Identifies the events that must be captured\n\n- Identifies who is responsible/accountable for performing these functions'
    component_components_3.purpose = ''
    component_components_3.status = ''
    component_components_3 = importer.save_or_locate(component_components_3)

    component_components_3.props.add(common_props_13)
    component_components_3.props.add(common_props_14)
    component_components_3.responsible_roles.add(component_responsible_roles_1)

    component_components_4 = components()
    component_components_4.uuid = UUID('fa39eb84-3014-46b4-b6bc-7da10527c262')
    component_components_4.created_at = dateutil.parser.parse("2023-02-28T15:48:24.834251+00:00")
    component_components_4.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.839014+00:00")
    component_components_4.remarks = ''
    component_components_4.type = 'process'
    component_components_4.title = 'Inventory Management Process'
    component_components_4.description = 'Describes how new components are introduced into the system - ensures monitoring teams know about every asset that should be producing logs, thus should be monitored.'
    component_components_4.purpose = ''
    component_components_4.status = ''
    component_components_4 = importer.save_or_locate(component_components_4)

    component_components_4.props.add(common_props_14)
    component_components_4.links.add(common_links_2)
    component_components_4.responsible_roles.add(component_responsible_roles_1)

    component_components_5 = components()
    component_components_5.uuid = UUID('e00acdcf-911b-437d-a42f-b0b558cc4f03')
    component_components_5.created_at = dateutil.parser.parse("2023-02-28T15:48:24.808606+00:00")
    component_components_5.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.817585+00:00")
    component_components_5.remarks = ''
    component_components_5.type = 'software'
    component_components_5.title = 'Logging Server'
    component_components_5.description = 'Provides a means for hosts to publish logged events to a central server.'
    component_components_5.purpose = ''
    component_components_5.status = ''
    component_components_5 = importer.save_or_locate(component_components_5)

    component_components_5.responsible_roles.add(component_responsible_roles_1)

    component_components_6 = components()
    component_components_6.uuid = UUID('659e207c-d50a-4944-a015-3c0dfe7cae10')
    component_components_6.created_at = dateutil.parser.parse("2023-02-28T15:40:45.982543+00:00")
    component_components_6.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.983006+00:00")
    component_components_6.remarks = ''
    component_components_6.type = 'policy'
    component_components_6.title = 'Organization of Information Security Policy'
    component_components_6.description = 'This Component Policy was automatically created during the import of Sample Security Catalog *for Demonstration* and Testing'
    component_components_6.purpose = 'This Component Policy was automatically created during the import of Sample Security Catalog *for Demonstration* and Testing'
    component_components_6.status = 'under-development'
    component_components_6 = importer.save_or_locate(component_components_6)

    component_components_7 = components()
    component_components_7.uuid = UUID('941e2a87-46f4-4b3e-9e87-bbd187091ca1')
    component_components_7.created_at = dateutil.parser.parse("2023-02-28T15:48:24.826222+00:00")
    component_components_7.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.832866+00:00")
    component_components_7.remarks = ''
    component_components_7.type = 'process'
    component_components_7.title = 'System Integration Process'
    component_components_7.description = 'Ensures proper integration into the enterprise as new systems are brought into production.'
    component_components_7.purpose = ''
    component_components_7.status = ''
    component_components_7 = importer.save_or_locate(component_components_7)

    component_components_7.props.add(common_props_14)
    component_components_7.links.add(common_links_1)
    component_components_7.responsible_roles.add(component_responsible_roles_1)

    # Processing model: ssp.models.system_ids

    from ssp.models import system_ids

    ssp_system_ids_1 = system_ids()
    ssp_system_ids_1.uuid = UUID('e8710c7e-446b-4174-a0f9-899e8aea6ba7')
    ssp_system_ids_1.created_at = dateutil.parser.parse("2023-02-28T15:48:24.763638+00:00")
    ssp_system_ids_1.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.763651+00:00")
    ssp_system_ids_1.identifier_type = ''
    ssp_system_ids_1.system_id = ''
    ssp_system_ids_1 = importer.save_or_locate(ssp_system_ids_1)

    # Processing model: ssp.models.information_type_ids

    from ssp.models import information_type_ids


    # Processing model: ssp.models.categorizations

    from ssp.models import categorizations


    # Processing model: ssp.models.information_type_impact_level

    from ssp.models import information_type_impact_level

    ssp_information_type_impact_level_1 = information_type_impact_level()
    ssp_information_type_impact_level_1.uuid = UUID('ab6a0e1c-d836-4825-9184-9e5d25eb2ceb')
    ssp_information_type_impact_level_1.created_at = dateutil.parser.parse("2023-02-28T15:48:24.777530+00:00")
    ssp_information_type_impact_level_1.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.779047+00:00")
    ssp_information_type_impact_level_1.remarks = ''
    ssp_information_type_impact_level_1.base = 'fips-199-moderate'
    ssp_information_type_impact_level_1.selected = None
    ssp_information_type_impact_level_1.adjustment_justification = None
    ssp_information_type_impact_level_1 = importer.save_or_locate(ssp_information_type_impact_level_1)

    ssp_information_type_impact_level_2 = information_type_impact_level()
    ssp_information_type_impact_level_2.uuid = UUID('24769048-0f53-46e9-a0e6-69ba1ca20f77')
    ssp_information_type_impact_level_2.created_at = dateutil.parser.parse("2023-02-28T15:48:24.779916+00:00")
    ssp_information_type_impact_level_2.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.780378+00:00")
    ssp_information_type_impact_level_2.remarks = ''
    ssp_information_type_impact_level_2.base = 'fips-199-low'
    ssp_information_type_impact_level_2.selected = None
    ssp_information_type_impact_level_2.adjustment_justification = None
    ssp_information_type_impact_level_2 = importer.save_or_locate(ssp_information_type_impact_level_2)

    # Processing model: ssp.models.information_types

    from ssp.models import information_types

    ssp_information_types_1 = information_types()
    ssp_information_types_1.uuid = UUID('b1d7b4ca-71fe-488d-8625-e1b2b5226c06')
    ssp_information_types_1.created_at = dateutil.parser.parse("2023-02-28T15:48:24.780915+00:00")
    ssp_information_types_1.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.780924+00:00")
    ssp_information_types_1.title = 'System and Network Monitoring'
    ssp_information_types_1.description = 'This system maintains historical logging and auditing information for all client devices connected to this system.'
    ssp_information_types_1.confidentiality_impact = ssp_information_type_impact_level_1
    ssp_information_types_1.integrity_impact = ssp_information_type_impact_level_1
    ssp_information_types_1.availability_impact = ssp_information_type_impact_level_2
    ssp_information_types_1 = importer.save_or_locate(ssp_information_types_1)

    # Processing model: ssp.models.systems_information

    from ssp.models import systems_information

    ssp_systems_information_1 = systems_information()
    ssp_systems_information_1.uuid = UUID('2b77e8ce-07ee-49e7-a52f-10b424053907')
    ssp_systems_information_1.created_at = dateutil.parser.parse("2023-02-28T15:48:24.775735+00:00")
    ssp_systems_information_1.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.782875+00:00")
    ssp_systems_information_1 = importer.save_or_locate(ssp_systems_information_1)

    ssp_systems_information_1.information_types.add(ssp_information_types_1)

    # Processing model: ssp.models.diagrams

    from ssp.models import diagrams


    # Processing model: ssp.models.authorization_boundaries

    from ssp.models import authorization_boundaries

    ssp_authorization_boundaries_1 = authorization_boundaries()
    ssp_authorization_boundaries_1.uuid = UUID('2f59f12a-db32-46f5-97e2-5c17c8634d79')
    ssp_authorization_boundaries_1.created_at = dateutil.parser.parse("2023-02-28T15:48:24.760521+00:00")
    ssp_authorization_boundaries_1.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.761357+00:00")
    ssp_authorization_boundaries_1.remarks = ''
    ssp_authorization_boundaries_1.description = 'The description of the authorization boundary would go here.'
    ssp_authorization_boundaries_1 = importer.save_or_locate(ssp_authorization_boundaries_1)

    # Processing model: ssp.models.network_architectures

    from ssp.models import network_architectures


    # Processing model: ssp.models.data_flows

    from ssp.models import data_flows


    # Processing model: ssp.models.system_characteristics

    from ssp.models import system_characteristics

    ssp_system_characteristics_1 = system_characteristics()
    ssp_system_characteristics_1.uuid = UUID('5dc462de-64ff-449c-aeb1-e498c7d7f335')
    ssp_system_characteristics_1.created_at = dateutil.parser.parse("2023-02-28T15:48:24.762523+00:00")
    ssp_system_characteristics_1.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.786113+00:00")
    ssp_system_characteristics_1.remarks = ''
    ssp_system_characteristics_1.system_name = 'Enterprise Logging and Auditing System'
    ssp_system_characteristics_1.system_name_short = None
    ssp_system_characteristics_1.description = 'This is an example of a system that provides enterprise logging and log auditing capabilities.'
    ssp_system_characteristics_1.date_authorized = None
    ssp_system_characteristics_1.security_sensitivity_level = 'moderate'
    ssp_system_characteristics_1.security_impact_level = None
    ssp_system_characteristics_1.security_objective_confidentiality = None
    ssp_system_characteristics_1.security_objective_integrity = None
    ssp_system_characteristics_1.security_objective_availability = None
    ssp_system_characteristics_1.status = None
    ssp_system_characteristics_1.authorization_boundary = ssp_authorization_boundaries_1
    ssp_system_characteristics_1.network_architecture = None
    ssp_system_characteristics_1.data_flow = None
    ssp_system_characteristics_1 = importer.save_or_locate(ssp_system_characteristics_1)

    ssp_system_characteristics_1.system_ids.add(ssp_system_ids_1)
    ssp_system_characteristics_1.props.add(common_props_10)
    ssp_system_characteristics_1.props.add(common_props_11)
    ssp_system_characteristics_1.system_information.add(ssp_systems_information_1)

    # Processing model: ssp.models.leveraged_authorizations

    from ssp.models import leveraged_authorizations


    # Processing model: ssp.models.system_functions

    from ssp.models import system_functions


    # Processing model: ssp.models.privileges

    from ssp.models import privileges


    # Processing model: ssp.models.users

    from ssp.models import users

    ssp_users_1 = users()
    ssp_users_1.uuid = UUID('9824089b-322c-456f-86c4-4111c4200f69')
    ssp_users_1.created_at = dateutil.parser.parse("2023-02-28T15:48:24.787655+00:00")
    ssp_users_1.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.794451+00:00")
    ssp_users_1.remarks = ''
    ssp_users_1.title = 'System Administrator'
    ssp_users_1.short_name = ''
    ssp_users_1.description = ''
    ssp_users_1 = importer.save_or_locate(ssp_users_1)

    ssp_users_1.props.add(common_props_12)
    ssp_users_1.role_ids.add(common_roles_19)

    ssp_users_2 = users()
    ssp_users_2.uuid = UUID('ae8de94c-835d-4303-83b1-114b6a117a07')
    ssp_users_2.created_at = dateutil.parser.parse("2023-02-28T15:48:24.797852+00:00")
    ssp_users_2.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.801313+00:00")
    ssp_users_2.remarks = ''
    ssp_users_2.title = 'Audit Team'
    ssp_users_2.short_name = ''
    ssp_users_2.description = ''
    ssp_users_2 = importer.save_or_locate(ssp_users_2)

    ssp_users_2.props.add(common_props_12)
    ssp_users_2.role_ids.add(common_roles_20)

    ssp_users_3 = users()
    ssp_users_3.uuid = UUID('372ce7a3-92b0-437e-a98c-24d29f9bfab8')
    ssp_users_3.created_at = dateutil.parser.parse("2023-02-28T15:48:24.802539+00:00")
    ssp_users_3.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.805836+00:00")
    ssp_users_3.remarks = ''
    ssp_users_3.title = 'Legal Department'
    ssp_users_3.short_name = ''
    ssp_users_3.description = ''
    ssp_users_3 = importer.save_or_locate(ssp_users_3)

    ssp_users_3.props.add(common_props_12)
    ssp_users_3.role_ids.add(common_roles_21)

    # Processing model: ssp.models.inventory_items

    from ssp.models import inventory_items

    ssp_inventory_items_1 = inventory_items()
    ssp_inventory_items_1.uuid = UUID('c9c32657-a0eb-4cf2-b5c1-20928983063c')
    ssp_inventory_items_1.created_at = dateutil.parser.parse("2023-02-28T15:48:24.848210+00:00")
    ssp_inventory_items_1.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.856878+00:00")
    ssp_inventory_items_1.remarks = ''
    ssp_inventory_items_1.description = 'The logging server.'
    ssp_inventory_items_1 = importer.save_or_locate(ssp_inventory_items_1)

    ssp_inventory_items_1.props.add(common_props_15)
    ssp_inventory_items_1.responsible_parties.add(common_responsible_parties_1)
    ssp_inventory_items_1.implemented_components.add(component_components_1)

    # Processing model: ssp.models.system_implementations

    from ssp.models import system_implementations

    ssp_system_implementations_1 = system_implementations()
    ssp_system_implementations_1.uuid = UUID('62b77247-eb21-4cb6-b991-d4b98a2167eb')
    ssp_system_implementations_1.created_at = dateutil.parser.parse("2023-02-28T15:48:24.786928+00:00")
    ssp_system_implementations_1.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.858265+00:00")
    ssp_system_implementations_1.remarks = 'This is a partial implementation that addresses the logging server portion of the auditing system.'
    ssp_system_implementations_1 = importer.save_or_locate(ssp_system_implementations_1)

    ssp_system_implementations_1.users.add(ssp_users_1)
    ssp_system_implementations_1.users.add(ssp_users_2)
    ssp_system_implementations_1.users.add(ssp_users_3)
    ssp_system_implementations_1.components.add(component_components_2)
    ssp_system_implementations_1.components.add(component_components_3)
    ssp_system_implementations_1.components.add(component_components_4)
    ssp_system_implementations_1.components.add(component_components_5)
    ssp_system_implementations_1.components.add(component_components_7)
    ssp_system_implementations_1.inventory_items.add(ssp_inventory_items_1)

    # Processing model: catalog.models.params

    from catalog.models import params

    catalog_params_1 = params()
    catalog_params_1.uuid = UUID('6b967542-b19b-4d27-bf32-a574611f6151')
    catalog_params_1.created_at = dateutil.parser.parse("2023-02-28T15:40:45.864075+00:00")
    catalog_params_1.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.864547+00:00")
    catalog_params_1.remarks = ''
    catalog_params_1.param_id = 's1.1.1-prm1'
    catalog_params_1.param_class = ''
    catalog_params_1.depends_on = None
    catalog_params_1.label = 'a choice from a selection'
    catalog_params_1.usage = ''
    catalog_params_1.values = ''
    catalog_params_1.select = ''
    catalog_params_1.how_many = ''
    catalog_params_1.choice = ''
    catalog_params_1 = importer.save_or_locate(catalog_params_1)

    catalog_params_2 = params()
    catalog_params_2.uuid = UUID('fd5e273a-80c7-4269-9f25-3302cfad1305')
    catalog_params_2.created_at = dateutil.parser.parse("2023-02-28T15:40:45.867377+00:00")
    catalog_params_2.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.867841+00:00")
    catalog_params_2.remarks = ''
    catalog_params_2.param_id = 's1.1.1-prm_2'
    catalog_params_2.param_class = ''
    catalog_params_2.depends_on = None
    catalog_params_2.label = 'a duration'
    catalog_params_2.usage = ''
    catalog_params_2.values = ''
    catalog_params_2.select = ''
    catalog_params_2.how_many = ''
    catalog_params_2.choice = ''
    catalog_params_2 = importer.save_or_locate(catalog_params_2)

    # Processing model: catalog.models.parts

    from catalog.models import parts

    catalog_parts_1 = parts()
    catalog_parts_1.uuid = UUID('772a1413-e21c-42ac-a135-829567c09161')
    catalog_parts_1.created_at = dateutil.parser.parse("2023-02-28T15:40:45.859237+00:00")
    catalog_parts_1.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.859603+00:00")
    catalog_parts_1.part_id = 's1.1_smt'
    catalog_parts_1.name = 'objective'
    catalog_parts_1.ns = ''
    catalog_parts_1.part_class = ''
    catalog_parts_1.title = ''
    catalog_parts_1.prose = 'To establish a management framework to initiate and control the implementation and operation of information security within the organization.'
    catalog_parts_1 = importer.save_or_locate(catalog_parts_1)

    catalog_parts_2 = parts()
    catalog_parts_2.uuid = UUID('adf174d6-c57b-45af-8b72-0d4b7261642f')
    catalog_parts_2.created_at = dateutil.parser.parse("2023-02-28T15:40:45.873297+00:00")
    catalog_parts_2.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.873701+00:00")
    catalog_parts_2.part_id = 's1.1.1_stm'
    catalog_parts_2.name = 'statement'
    catalog_parts_2.ns = ''
    catalog_parts_2.part_class = ''
    catalog_parts_2.title = ''
    catalog_parts_2.prose = 'All information security responsibilities should be defined and allocated.\n\nA value has been assigned to {{ insert: param, s1.1.1-prm11 }}.\n\nA cross link has been established with a choppy syntax: [(choppy)](#s1.2).'
    catalog_parts_2 = importer.save_or_locate(catalog_parts_2)

    catalog_parts_3 = parts()
    catalog_parts_3.uuid = UUID('1e8227e5-3748-4cf8-8b9c-c202885eb84e')
    catalog_parts_3.created_at = dateutil.parser.parse("2023-02-28T15:40:45.875591+00:00")
    catalog_parts_3.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.883009+00:00")
    catalog_parts_3.part_id = 's1.1.1_gdn'
    catalog_parts_3.name = 'guidance'
    catalog_parts_3.ns = ''
    catalog_parts_3.part_class = ''
    catalog_parts_3.title = ''
    catalog_parts_3.prose = ''
    catalog_parts_3 = importer.save_or_locate(catalog_parts_3)

    catalog_parts_4 = parts()
    catalog_parts_4.uuid = UUID('b743c988-c9c1-4305-ae6a-81794757059d')
    catalog_parts_4.created_at = dateutil.parser.parse("2023-02-28T15:40:45.876289+00:00")
    catalog_parts_4.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.876643+00:00")
    catalog_parts_4.part_id = 's1.1.1_gdn.1'
    catalog_parts_4.name = 'item'
    catalog_parts_4.ns = ''
    catalog_parts_4.part_class = ''
    catalog_parts_4.title = ''
    catalog_parts_4.prose = 'Allocation of information security responsibilities should be done in accordance with the information security policies. Responsibilities for the protection of individual assets and for carrying out specific information security processes should be identified. Responsibilities for information security risk management activities and in particular for acceptance of residual risks should be defined. These responsibilities should be supplemented, where necessary, with more detailed guidance for specific sites and information processing facilities. Local responsibilities for the protection of assets and for carrying out specific security processes should be defined.'
    catalog_parts_4 = importer.save_or_locate(catalog_parts_4)

    catalog_parts_5 = parts()
    catalog_parts_5.uuid = UUID('5384304b-d718-455d-93af-ab36227a636b')
    catalog_parts_5.created_at = dateutil.parser.parse("2023-02-28T15:40:45.879429+00:00")
    catalog_parts_5.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.879771+00:00")
    catalog_parts_5.part_id = 's1.1.1_gdn.2'
    catalog_parts_5.name = 'item'
    catalog_parts_5.ns = ''
    catalog_parts_5.part_class = ''
    catalog_parts_5.title = ''
    catalog_parts_5.prose = 'Individuals with allocated information security responsibilities may delegate security tasks to others. Nevertheless they remain accountable and should determine that any delegated tasks have been correctly performed.'
    catalog_parts_5 = importer.save_or_locate(catalog_parts_5)

    catalog_parts_6 = parts()
    catalog_parts_6.uuid = UUID('f7fbc580-d95e-4a4e-85b6-b4d7ad9dc98a')
    catalog_parts_6.created_at = dateutil.parser.parse("2023-02-28T15:40:45.881181+00:00")
    catalog_parts_6.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.881547+00:00")
    catalog_parts_6.part_id = 's1.1.1_gdn.3'
    catalog_parts_6.name = 'item'
    catalog_parts_6.ns = ''
    catalog_parts_6.part_class = ''
    catalog_parts_6.title = ''
    catalog_parts_6.prose = 'Areas for which individuals are responsible should be stated. In particular the following should take place:\n\n1. the assets and information security processes should be identified and defined;\n1. the entity responsible for each asset or information security process should be assigned and the details of this responsibility should be documented;\n1. authorization levels should be defined and documented;\n1. to be able to fulfil responsibilities in the information security area the appointed individuals should be competent in the area and be given opportunities to keep up to date with developments;\n1. coordination and oversight of information security aspects of supplier relationships should be identified and documented.\n'
    catalog_parts_6 = importer.save_or_locate(catalog_parts_6)

    catalog_parts_7 = parts()
    catalog_parts_7.uuid = UUID('18213aab-324d-4a86-a002-2ce60107466a')
    catalog_parts_7.created_at = dateutil.parser.parse("2023-02-28T15:40:45.884351+00:00")
    catalog_parts_7.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.887984+00:00")
    catalog_parts_7.part_id = 's1.1.1_inf'
    catalog_parts_7.name = 'information'
    catalog_parts_7.ns = ''
    catalog_parts_7.part_class = ''
    catalog_parts_7.title = ''
    catalog_parts_7.prose = 'Many organizations appoint an information security manager to take overall responsibility for the development and implementation of information security and to support the identification of controls.\n\nHowever, responsibility for resourcing and implementing the controls will often remain with individual managers. One common practice is to appoint an owner for each asset who then becomes responsible for its day-to-day protection.'
    catalog_parts_7 = importer.save_or_locate(catalog_parts_7)

    catalog_parts_7.props.add(common_props_4)

    catalog_parts_8 = parts()
    catalog_parts_8.uuid = UUID('edc8c60e-9615-4005-bc08-8192e58f01b0')
    catalog_parts_8.created_at = dateutil.parser.parse("2023-02-28T15:40:45.895836+00:00")
    catalog_parts_8.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.896173+00:00")
    catalog_parts_8.part_id = 's1.1.2_stm'
    catalog_parts_8.name = 'statement'
    catalog_parts_8.ns = ''
    catalog_parts_8.part_class = ''
    catalog_parts_8.title = ''
    catalog_parts_8.prose = 'Conflicting duties and areas of responsibility should be segregated to reduce opportunities for unauthorized or unintentional modification or misuse of the organization’s assets.'
    catalog_parts_8 = importer.save_or_locate(catalog_parts_8)

    catalog_parts_9 = parts()
    catalog_parts_9.uuid = UUID('276dfdac-7d30-4c3e-99e7-58615470b74b')
    catalog_parts_9.created_at = dateutil.parser.parse("2023-02-28T15:40:45.897505+00:00")
    catalog_parts_9.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.901503+00:00")
    catalog_parts_9.part_id = 's1.1.2_gdn'
    catalog_parts_9.name = 'guidance'
    catalog_parts_9.ns = ''
    catalog_parts_9.part_class = ''
    catalog_parts_9.title = ''
    catalog_parts_9.prose = ''
    catalog_parts_9 = importer.save_or_locate(catalog_parts_9)

    catalog_parts_10 = parts()
    catalog_parts_10.uuid = UUID('39e0f741-762c-4199-ae06-a9894f9a2d69')
    catalog_parts_10.created_at = dateutil.parser.parse("2023-02-28T15:40:45.898116+00:00")
    catalog_parts_10.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.898471+00:00")
    catalog_parts_10.part_id = 's1.1.2_gdn.1'
    catalog_parts_10.name = 'item'
    catalog_parts_10.ns = ''
    catalog_parts_10.part_class = ''
    catalog_parts_10.title = ''
    catalog_parts_10.prose = 'Care should be taken that no single person can access, modify or use assets without authorization or detection. The initiation of an event should be separated from its authorization. The possibility of collusion should be considered in designing the controls.'
    catalog_parts_10 = importer.save_or_locate(catalog_parts_10)

    catalog_parts_11 = parts()
    catalog_parts_11.uuid = UUID('bd1e837d-36fe-4dc2-b793-39d18c59a3d8')
    catalog_parts_11.created_at = dateutil.parser.parse("2023-02-28T15:40:45.899731+00:00")
    catalog_parts_11.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.900070+00:00")
    catalog_parts_11.part_id = 's1.1.2_gdn.2'
    catalog_parts_11.name = 'item'
    catalog_parts_11.ns = ''
    catalog_parts_11.part_class = ''
    catalog_parts_11.title = ''
    catalog_parts_11.prose = 'Small organizations may find segregation of duties difficult to achieve, but the principle should be applied as far as is possible and practicable. Whenever it is difficult to segregate, other controls such as monitoring of activities, audit trails and management supervision should be considered.'
    catalog_parts_11 = importer.save_or_locate(catalog_parts_11)

    catalog_parts_12 = parts()
    catalog_parts_12.uuid = UUID('58e59ef3-3f06-4cd6-93f6-47816e9198a2')
    catalog_parts_12.created_at = dateutil.parser.parse("2023-02-28T15:40:45.902741+00:00")
    catalog_parts_12.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.903105+00:00")
    catalog_parts_12.part_id = 's1.1.2_inf'
    catalog_parts_12.name = 'information'
    catalog_parts_12.ns = ''
    catalog_parts_12.part_class = ''
    catalog_parts_12.title = ''
    catalog_parts_12.prose = 'Segregation of duties is a method for reducing the risk of accidental or deliberate misuse of an organization’s assets.'
    catalog_parts_12 = importer.save_or_locate(catalog_parts_12)

    catalog_parts_13 = parts()
    catalog_parts_13.uuid = UUID('696e41c8-e38d-4f12-8a89-a6c814ff945d')
    catalog_parts_13.created_at = dateutil.parser.parse("2023-02-28T15:40:45.915312+00:00")
    catalog_parts_13.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.915687+00:00")
    catalog_parts_13.part_id = 's2.1_smt'
    catalog_parts_13.name = 'objective'
    catalog_parts_13.ns = ''
    catalog_parts_13.part_class = ''
    catalog_parts_13.title = ''
    catalog_parts_13.prose = 'To limit access to information and information processing facilities.'
    catalog_parts_13 = importer.save_or_locate(catalog_parts_13)

    catalog_parts_14 = parts()
    catalog_parts_14.uuid = UUID('f88ee8bf-19dd-4b2f-ba18-60bace404823')
    catalog_parts_14.created_at = dateutil.parser.parse("2023-02-28T15:40:45.920215+00:00")
    catalog_parts_14.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.920604+00:00")
    catalog_parts_14.part_id = 's2.1.1_stm'
    catalog_parts_14.name = 'statement'
    catalog_parts_14.ns = ''
    catalog_parts_14.part_class = ''
    catalog_parts_14.title = ''
    catalog_parts_14.prose = 'An access control policy should be established, documented and reviewed based on business and information security requirements.'
    catalog_parts_14 = importer.save_or_locate(catalog_parts_14)

    catalog_parts_15 = parts()
    catalog_parts_15.uuid = UUID('d646efb5-8fa2-4a49-85ed-aacfd4078e7f')
    catalog_parts_15.created_at = dateutil.parser.parse("2023-02-28T15:40:45.921989+00:00")
    catalog_parts_15.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.930081+00:00")
    catalog_parts_15.part_id = 's2.1.1_gdn'
    catalog_parts_15.name = 'guidance'
    catalog_parts_15.ns = ''
    catalog_parts_15.part_class = ''
    catalog_parts_15.title = ''
    catalog_parts_15.prose = ''
    catalog_parts_15 = importer.save_or_locate(catalog_parts_15)

    catalog_parts_16 = parts()
    catalog_parts_16.uuid = UUID('ff62fb32-3f52-4f68-b4d3-bb0dbcb43f9b')
    catalog_parts_16.created_at = dateutil.parser.parse("2023-02-28T15:40:45.922592+00:00")
    catalog_parts_16.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.922965+00:00")
    catalog_parts_16.part_id = 's2.1.1_gdn.1'
    catalog_parts_16.name = 'item'
    catalog_parts_16.ns = ''
    catalog_parts_16.part_class = ''
    catalog_parts_16.title = ''
    catalog_parts_16.prose = 'Asset owners should determine appropriate access control rules, access rights and restrictions for specific user roles towards their assets, with the amount of detail and the strictness of the controls reflecting the associated information security risks.'
    catalog_parts_16 = importer.save_or_locate(catalog_parts_16)

    catalog_parts_17 = parts()
    catalog_parts_17.uuid = UUID('ffd79510-d209-42d4-a091-91ab430b8c98')
    catalog_parts_17.created_at = dateutil.parser.parse("2023-02-28T15:40:45.924380+00:00")
    catalog_parts_17.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.924778+00:00")
    catalog_parts_17.part_id = 's2.1.1_gdn.2'
    catalog_parts_17.name = 'item'
    catalog_parts_17.ns = ''
    catalog_parts_17.part_class = ''
    catalog_parts_17.title = ''
    catalog_parts_17.prose = 'Access controls are both logical and physical and these should be considered together.'
    catalog_parts_17 = importer.save_or_locate(catalog_parts_17)

    catalog_parts_18 = parts()
    catalog_parts_18.uuid = UUID('f17c6721-7c92-486e-88d9-459a904114fb')
    catalog_parts_18.created_at = dateutil.parser.parse("2023-02-28T15:40:45.926388+00:00")
    catalog_parts_18.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.926811+00:00")
    catalog_parts_18.part_id = 's2.1.1_gdn.3'
    catalog_parts_18.name = 'item'
    catalog_parts_18.ns = ''
    catalog_parts_18.part_class = ''
    catalog_parts_18.title = ''
    catalog_parts_18.prose = 'Users and service providers should be given a clear statement of the business requirements to be met by access controls.'
    catalog_parts_18 = importer.save_or_locate(catalog_parts_18)

    catalog_parts_19 = parts()
    catalog_parts_19.uuid = UUID('17ffc58e-44bc-4ac7-b4bd-2b3cea079f88')
    catalog_parts_19.created_at = dateutil.parser.parse("2023-02-28T15:40:45.928317+00:00")
    catalog_parts_19.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.928672+00:00")
    catalog_parts_19.part_id = 's2.1.1_gdn.4'
    catalog_parts_19.name = 'item'
    catalog_parts_19.ns = ''
    catalog_parts_19.part_class = ''
    catalog_parts_19.title = ''
    catalog_parts_19.prose = 'The policy should take account of the following:\n\n1. security requirements of business applications;\n1. policies for information dissemination and authorization, e.g. the need-to-know principle and information security levels and classification of information;\n1. consistency between the access rights and information classification policies of systems and networks;\n1. relevant legislation and any contractual obligations regarding limitation of access to data or services;\n1. management of access rights in a distributed and networked environment which recognizes all types of connections available;\n1. segregation of access control roles, e.g. access request, access authorization, access administration;\n1. requirements for formal authorization of access requests;\n1. requirements for periodic review of access rights;\n1. removal of access rights;\n1. archiving of records of all significant events concerning the use and management of user identities and secret authentication information;,\n1. roles with privileged access.\n'
    catalog_parts_19 = importer.save_or_locate(catalog_parts_19)

    catalog_parts_20 = parts()
    catalog_parts_20.uuid = UUID('d1d9bf10-2fc4-481a-aef5-1d0c995868be')
    catalog_parts_20.created_at = dateutil.parser.parse("2023-02-28T15:40:45.931405+00:00")
    catalog_parts_20.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.939038+00:00")
    catalog_parts_20.part_id = 's2.1.1_stm'
    catalog_parts_20.name = 'information'
    catalog_parts_20.ns = ''
    catalog_parts_20.part_class = ''
    catalog_parts_20.title = ''
    catalog_parts_20.prose = ''
    catalog_parts_20 = importer.save_or_locate(catalog_parts_20)

    catalog_parts_21 = parts()
    catalog_parts_21.uuid = UUID('92a64eb0-7584-4bf6-9c7b-0658955e2b16')
    catalog_parts_21.created_at = dateutil.parser.parse("2023-02-28T15:40:45.932035+00:00")
    catalog_parts_21.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.932406+00:00")
    catalog_parts_21.part_id = 's2.1.1_stm.1'
    catalog_parts_21.name = 'item'
    catalog_parts_21.ns = ''
    catalog_parts_21.part_class = ''
    catalog_parts_21.title = ''
    catalog_parts_21.prose = 'Care should be taken when specifying access control rules to consider:\n\n1. establishing rules based on the premise “Everything is generally forbidden unless expressly permitted” rather than the weaker rule “Everything is generally permitted unless expressly forbidden”;\n1. changes in information labels that are initiated automatically by information processing facilities and those initiated at the discretion of a user;\n1. changes in user permissions that are initiated automatically by the information system and those initiated by an administrator;\n1. rules which require specific approval before enactment and those which do not.\n'
    catalog_parts_21 = importer.save_or_locate(catalog_parts_21)

    catalog_parts_22 = parts()
    catalog_parts_22.uuid = UUID('d017fa52-2e07-429e-8164-0698452f6384')
    catalog_parts_22.created_at = dateutil.parser.parse("2023-02-28T15:40:45.933802+00:00")
    catalog_parts_22.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.934191+00:00")
    catalog_parts_22.part_id = 's2.1.1_stm.2'
    catalog_parts_22.name = 'item'
    catalog_parts_22.ns = ''
    catalog_parts_22.part_class = ''
    catalog_parts_22.title = ''
    catalog_parts_22.prose = 'Access control rules should be supported by formal procedures and defined responsibilities.'
    catalog_parts_22 = importer.save_or_locate(catalog_parts_22)

    catalog_parts_23 = parts()
    catalog_parts_23.uuid = UUID('c23b2993-648e-47ef-8f3d-7099f1b33668')
    catalog_parts_23.created_at = dateutil.parser.parse("2023-02-28T15:40:45.935505+00:00")
    catalog_parts_23.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.935871+00:00")
    catalog_parts_23.part_id = 's2.1.1_stm.3'
    catalog_parts_23.name = 'item'
    catalog_parts_23.ns = ''
    catalog_parts_23.part_class = ''
    catalog_parts_23.title = ''
    catalog_parts_23.prose = 'Role based access control is an approach used successfully by many organizations to link access rights with business roles.'
    catalog_parts_23 = importer.save_or_locate(catalog_parts_23)

    catalog_parts_24 = parts()
    catalog_parts_24.uuid = UUID('45166b61-4dd6-4eff-b8df-09b602fa16ed')
    catalog_parts_24.created_at = dateutil.parser.parse("2023-02-28T15:40:45.937195+00:00")
    catalog_parts_24.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.937544+00:00")
    catalog_parts_24.part_id = 's2.1.1_stm.4'
    catalog_parts_24.name = 'item'
    catalog_parts_24.ns = ''
    catalog_parts_24.part_class = ''
    catalog_parts_24.title = ''
    catalog_parts_24.prose = 'Two of the frequent principles directing the access control policy are:\n\n1. Need-to-know: you are only granted access to the information you need to perform your tasks (different tasks/roles mean different need-to-know and hence different access profile);\n1. Need-to-use: you are only granted access to the information processing facilities (IT equipment, applications, procedures, rooms) you need to perform your task/job/role.\n'
    catalog_parts_24 = importer.save_or_locate(catalog_parts_24)

    catalog_parts_25 = parts()
    catalog_parts_25.uuid = UUID('deff7bb5-88ff-4622-aa8c-73de19f8a0e6')
    catalog_parts_25.created_at = dateutil.parser.parse("2023-02-28T15:40:45.944521+00:00")
    catalog_parts_25.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.944866+00:00")
    catalog_parts_25.part_id = 's2.1.2_stm'
    catalog_parts_25.name = 'statement'
    catalog_parts_25.ns = ''
    catalog_parts_25.part_class = ''
    catalog_parts_25.title = ''
    catalog_parts_25.prose = 'Users should only be provided with access to the network and network services that they have been specifically authorized to use.'
    catalog_parts_25 = importer.save_or_locate(catalog_parts_25)

    catalog_parts_26 = parts()
    catalog_parts_26.uuid = UUID('c3fa3ffe-c3fa-4075-8050-8e0fd8eadab1')
    catalog_parts_26.created_at = dateutil.parser.parse("2023-02-28T15:40:45.946094+00:00")
    catalog_parts_26.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.950545+00:00")
    catalog_parts_26.part_id = 's2.1.2_gdn'
    catalog_parts_26.name = 'guidance'
    catalog_parts_26.ns = ''
    catalog_parts_26.part_class = ''
    catalog_parts_26.title = ''
    catalog_parts_26.prose = ''
    catalog_parts_26 = importer.save_or_locate(catalog_parts_26)

    catalog_parts_27 = parts()
    catalog_parts_27.uuid = UUID('ed609691-2585-4e58-9d4c-d35e8e51d8a7')
    catalog_parts_27.created_at = dateutil.parser.parse("2023-02-28T15:40:45.946743+00:00")
    catalog_parts_27.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.947100+00:00")
    catalog_parts_27.part_id = 's2.1.2_gdn.1'
    catalog_parts_27.name = 'item'
    catalog_parts_27.ns = ''
    catalog_parts_27.part_class = ''
    catalog_parts_27.title = ''
    catalog_parts_27.prose = 'A policy should be formulated concerning the use of networks and network services. This policy should cover:\n\n1. the networks and network services which are allowed to be accessed;\n1. authorization procedures for determining who is allowed to access which networks and networked services;\n1. management controls and procedures to protect access to network connections and network services;\n1. the means used to access networks and network services (e.g. use of VPN or wireless network);\n1. user authentication requirements for accessing various network services;\n1. monitoring of the use of network service\n'
    catalog_parts_27 = importer.save_or_locate(catalog_parts_27)

    catalog_parts_28 = parts()
    catalog_parts_28.uuid = UUID('f2c9be4f-37c6-453a-a616-c83d7df4d648')
    catalog_parts_28.created_at = dateutil.parser.parse("2023-02-28T15:40:45.948494+00:00")
    catalog_parts_28.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.948839+00:00")
    catalog_parts_28.part_id = 's2.1.2_gdn.2'
    catalog_parts_28.name = 'item'
    catalog_parts_28.ns = ''
    catalog_parts_28.part_class = ''
    catalog_parts_28.title = ''
    catalog_parts_28.prose = 'The policy on the use of network services should be consistent with the organization’s access control policy'
    catalog_parts_28 = importer.save_or_locate(catalog_parts_28)

    # Processing model: catalog.models.controls

    from catalog.models import controls

    catalog_controls_1 = controls()
    catalog_controls_1.uuid = UUID('c917d796-1b5f-4994-9366-d4eadd05ba72')
    catalog_controls_1.created_at = dateutil.parser.parse("2023-02-28T15:40:45.861257+00:00")
    catalog_controls_1.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.991072+00:00")
    catalog_controls_1.control_id = 's1.1.1'
    catalog_controls_1.control_class = ''
    catalog_controls_1.title = 'Information security roles and responsibilities'
    catalog_controls_1.sort_id = 's1.1.1'
    catalog_controls_1 = importer.save_or_locate(catalog_controls_1)

    catalog_controls_1.params.add(catalog_params_1)
    catalog_controls_1.params.add(catalog_params_2)
    catalog_controls_1.props.add(common_props_3)
    catalog_controls_1.parts.add(catalog_parts_2)
    catalog_controls_1.parts.add(catalog_parts_3)
    catalog_controls_1.parts.add(catalog_parts_7)

    catalog_controls_2 = controls()
    catalog_controls_2.uuid = UUID('616c30d2-fea4-4846-9666-56b21fd33a97')
    catalog_controls_2.created_at = dateutil.parser.parse("2023-02-28T15:40:45.893284+00:00")
    catalog_controls_2.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.992846+00:00")
    catalog_controls_2.control_id = 's1.1.2'
    catalog_controls_2.control_class = ''
    catalog_controls_2.title = 'Segregation of duties'
    catalog_controls_2.sort_id = 's1.1.2'
    catalog_controls_2 = importer.save_or_locate(catalog_controls_2)

    catalog_controls_2.props.add(common_props_5)
    catalog_controls_2.parts.add(catalog_parts_8)
    catalog_controls_2.parts.add(catalog_parts_9)
    catalog_controls_2.parts.add(catalog_parts_12)

    catalog_controls_3 = controls()
    catalog_controls_3.uuid = UUID('76cb7cc8-5dff-4b2c-8ec8-db251db14677')
    catalog_controls_3.created_at = dateutil.parser.parse("2023-02-28T15:40:45.917437+00:00")
    catalog_controls_3.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.994362+00:00")
    catalog_controls_3.control_id = 's2.1.1'
    catalog_controls_3.control_class = ''
    catalog_controls_3.title = 'Access control policy'
    catalog_controls_3.sort_id = 's2.1.1'
    catalog_controls_3 = importer.save_or_locate(catalog_controls_3)

    catalog_controls_3.props.add(common_props_8)
    catalog_controls_3.parts.add(catalog_parts_14)
    catalog_controls_3.parts.add(catalog_parts_15)
    catalog_controls_3.parts.add(catalog_parts_20)

    catalog_controls_4 = controls()
    catalog_controls_4.uuid = UUID('faad26c9-8ec1-44a6-8434-0ba21e3f3cb8')
    catalog_controls_4.created_at = dateutil.parser.parse("2023-02-28T15:40:45.941808+00:00")
    catalog_controls_4.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.995776+00:00")
    catalog_controls_4.control_id = 's2.1.2'
    catalog_controls_4.control_class = ''
    catalog_controls_4.title = 'Access to networks and network services'
    catalog_controls_4.sort_id = 's2.1.2'
    catalog_controls_4 = importer.save_or_locate(catalog_controls_4)

    catalog_controls_4.props.add(common_props_9)
    catalog_controls_4.parts.add(catalog_parts_25)
    catalog_controls_4.parts.add(catalog_parts_26)

    # Processing model: catalog.models.groups

    from catalog.models import groups

    catalog_groups_1 = groups()
    catalog_groups_1.uuid = UUID('35c6498a-ad4e-4925-8329-7e3638a16a1d')
    catalog_groups_1.created_at = dateutil.parser.parse("2023-02-28T15:40:45.853160+00:00")
    catalog_groups_1.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.907173+00:00")
    catalog_groups_1.group_id = 's1'
    catalog_groups_1.group_class = ''
    catalog_groups_1.title = 'Organization of Information Security'
    catalog_groups_1 = importer.save_or_locate(catalog_groups_1)

    catalog_groups_1.props.add(common_props_1)

    catalog_groups_2 = groups()
    catalog_groups_2.uuid = UUID('8643818d-8530-4809-9c59-0bd67ed82b36')
    catalog_groups_2.created_at = dateutil.parser.parse("2023-02-28T15:40:45.856406+00:00")
    catalog_groups_2.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.905855+00:00")
    catalog_groups_2.group_id = 's1.1'
    catalog_groups_2.group_class = ''
    catalog_groups_2.title = 'Internal Organization'
    catalog_groups_2 = importer.save_or_locate(catalog_groups_2)

    catalog_groups_2.props.add(common_props_2)
    catalog_groups_2.parts.add(catalog_parts_1)
    catalog_groups_2.controls.add(catalog_controls_1)
    catalog_groups_2.controls.add(catalog_controls_2)

    catalog_groups_3 = groups()
    catalog_groups_3.uuid = UUID('584ebd01-2715-44ea-b57e-b8f528fb57ea')
    catalog_groups_3.created_at = dateutil.parser.parse("2023-02-28T15:40:45.910278+00:00")
    catalog_groups_3.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.955953+00:00")
    catalog_groups_3.group_id = 's2'
    catalog_groups_3.group_class = ''
    catalog_groups_3.title = 'Access control'
    catalog_groups_3 = importer.save_or_locate(catalog_groups_3)

    catalog_groups_3.props.add(common_props_6)

    catalog_groups_4 = groups()
    catalog_groups_4.uuid = UUID('37b85345-8a54-468c-8a40-0f62c5d62f24')
    catalog_groups_4.created_at = dateutil.parser.parse("2023-02-28T15:40:45.912770+00:00")
    catalog_groups_4.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.954160+00:00")
    catalog_groups_4.group_id = 's2.1'
    catalog_groups_4.group_class = ''
    catalog_groups_4.title = 'Business requirements of access control'
    catalog_groups_4 = importer.save_or_locate(catalog_groups_4)

    catalog_groups_4.props.add(common_props_7)
    catalog_groups_4.parts.add(catalog_parts_13)
    catalog_groups_4.controls.add(catalog_controls_3)
    catalog_groups_4.controls.add(catalog_controls_4)

    # Processing model: catalog.models.catalogs

    from catalog.models import catalogs

    catalog_catalogs_1 = catalogs()
    catalog_catalogs_1.created_at = dateutil.parser.parse("2023-02-28T15:40:45.851944+00:00")
    catalog_catalogs_1.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.958244+00:00")
    catalog_catalogs_1.uuid = '74c8ba1e-5cd4-4ad1-bbfd-d888e2f6c724'
    catalog_catalogs_1.metadata = common_metadata_1
    catalog_catalogs_1.back_matter = None
    catalog_catalogs_1 = importer.save_or_locate(catalog_catalogs_1)

    catalog_catalogs_1.groups.add(catalog_groups_1)
    catalog_catalogs_1.groups.add(catalog_groups_3)

    # Processing model: component.models.responsibilities

    from component.models import responsibilities


    # Processing model: component.models.export

    from component.models import export


    # Processing model: component.models.inherited

    from component.models import inherited


    # Processing model: ctrl_profile.models.imports

    from ctrl_profile.models import imports

    ctrl_profile_imports_1 = imports()
    ctrl_profile_imports_1.uuid = UUID('73fe31c6-5a46-45aa-bc59-068b51f4b3c0')
    ctrl_profile_imports_1.created_at = dateutil.parser.parse("2023-02-28T15:40:45.979479+00:00")
    ctrl_profile_imports_1.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.979491+00:00")
    ctrl_profile_imports_1.remarks = ''
    ctrl_profile_imports_1.href = 'https://http://localhost:8000/common/p/74c8ba1e-5cd4-4ad1-bbfd-d888e2f6c724'
    ctrl_profile_imports_1.import_type = 'catalog'
    ctrl_profile_imports_1.include_all = True
    ctrl_profile_imports_1 = importer.save_or_locate(ctrl_profile_imports_1)

    # Processing model: ctrl_profile.models.modify

    from ctrl_profile.models import modify


    # Processing model: ctrl_profile.models.profiles

    from ctrl_profile.models import profiles

    ctrl_profile_profiles_1 = profiles()
    ctrl_profile_profiles_1.uuid = UUID('9722f354-8c19-48a9-9f3f-65d473fa967d')
    ctrl_profile_profiles_1.created_at = dateutil.parser.parse("2023-02-28T15:40:45.959314+00:00")
    ctrl_profile_profiles_1.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.980886+00:00")
    ctrl_profile_profiles_1.remarks = ''
    ctrl_profile_profiles_1.metadata = common_metadata_2
    ctrl_profile_profiles_1.merge = None
    ctrl_profile_profiles_1.modify = None
    ctrl_profile_profiles_1.back_matter = None
    ctrl_profile_profiles_1 = importer.save_or_locate(ctrl_profile_profiles_1)

    ctrl_profile_profiles_1.imports.add(ctrl_profile_imports_1)

    # Processing model: ssp.models.import_profiles

    from ssp.models import import_profiles

    ssp_import_profiles_1 = import_profiles()
    ssp_import_profiles_1.uuid = UUID('93d4d033-15d5-454c-b438-8731c05b803c')
    ssp_import_profiles_1.created_at = dateutil.parser.parse("2023-02-28T15:48:24.755700+00:00")
    ssp_import_profiles_1.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.756845+00:00")
    ssp_import_profiles_1.remarks = ''
    ssp_import_profiles_1.href = '../../../nist.gov/SP800-53/rev4/json/NIST_SP-800-53_rev4_MODERATE-baseline_profile.json'
    ssp_import_profiles_1.local_profile = None
    ssp_import_profiles_1 = importer.save_or_locate(ssp_import_profiles_1)

    # Processing model: component.models.satisfied

    from component.models import satisfied


    # Processing model: ssp.models.system_security_plans

    from ssp.models import system_security_plans

    ssp_system_security_plans_1 = system_security_plans()
    ssp_system_security_plans_1.uuid = UUID('cff8385f-108e-40a5-8f7a-82f3dc0eaba8')
    ssp_system_security_plans_1.created_at = dateutil.parser.parse("2023-02-28T15:48:24.861902+00:00")
    ssp_system_security_plans_1.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.864629+00:00")
    ssp_system_security_plans_1.remarks = ''
    ssp_system_security_plans_1.metadata = common_metadata_3
    ssp_system_security_plans_1.import_profile = ssp_import_profiles_1
    ssp_system_security_plans_1.system_characteristics = ssp_system_characteristics_1
    ssp_system_security_plans_1.system_implementation = ssp_system_implementations_1
    ssp_system_security_plans_1.back_matter = None
    ssp_system_security_plans_1 = importer.save_or_locate(ssp_system_security_plans_1)

    # Processing model: component.models.parameters

    from component.models import parameters


    # Processing model: component.models.statements

    from component.models import statements


    # Processing model: component.models.by_components

    from component.models import by_components


    # Processing model: component.models.implemented_requirements

    from component.models import implemented_requirements

    component_implemented_requirements_1 = implemented_requirements()
    component_implemented_requirements_1.uuid = UUID('7e1aa60f-8059-4289-a421-a5a0cfe4e331')
    component_implemented_requirements_1.created_at = dateutil.parser.parse("2023-02-28T15:40:45.989685+00:00")
    component_implemented_requirements_1.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.989699+00:00")
    component_implemented_requirements_1.remarks = ''
    component_implemented_requirements_1.control_id = catalog_controls_1
    component_implemented_requirements_1 = importer.save_or_locate(component_implemented_requirements_1)

    component_implemented_requirements_2 = implemented_requirements()
    component_implemented_requirements_2.uuid = UUID('503fd863-a095-43bd-aa49-6bb92e7b7f35')
    component_implemented_requirements_2.created_at = dateutil.parser.parse("2023-02-28T15:40:45.992040+00:00")
    component_implemented_requirements_2.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.992053+00:00")
    component_implemented_requirements_2.remarks = ''
    component_implemented_requirements_2.control_id = catalog_controls_2
    component_implemented_requirements_2 = importer.save_or_locate(component_implemented_requirements_2)

    component_implemented_requirements_3 = implemented_requirements()
    component_implemented_requirements_3.uuid = UUID('7a3e6b60-7122-4806-a097-1dd22dd95469')
    component_implemented_requirements_3.created_at = dateutil.parser.parse("2023-02-28T15:40:45.993620+00:00")
    component_implemented_requirements_3.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.993630+00:00")
    component_implemented_requirements_3.remarks = ''
    component_implemented_requirements_3.control_id = catalog_controls_3
    component_implemented_requirements_3 = importer.save_or_locate(component_implemented_requirements_3)

    component_implemented_requirements_4 = implemented_requirements()
    component_implemented_requirements_4.uuid = UUID('f61e63f0-6016-448f-88ba-20a5484947ad')
    component_implemented_requirements_4.created_at = dateutil.parser.parse("2023-02-28T15:40:45.995077+00:00")
    component_implemented_requirements_4.updated_at = dateutil.parser.parse("2023-02-28T15:40:45.995086+00:00")
    component_implemented_requirements_4.remarks = ''
    component_implemented_requirements_4.control_id = catalog_controls_4
    component_implemented_requirements_4 = importer.save_or_locate(component_implemented_requirements_4)

    # Processing model: component.models.control_implementations

    from component.models import control_implementations

    component_control_implementations_1 = control_implementations()
    component_control_implementations_1.uuid = UUID('6f17a427-0f42-49c2-a29a-498ff1eb9145')
    component_control_implementations_1.created_at = dateutil.parser.parse("2023-02-28T15:48:24.859077+00:00")
    component_control_implementations_1.updated_at = dateutil.parser.parse("2023-02-28T15:48:24.861449+00:00")
    component_control_implementations_1.remarks = ''
    component_control_implementations_1.description = 'This is the control implementation for the system.'
    component_control_implementations_1.component = None
    component_control_implementations_1 = importer.save_or_locate(component_control_implementations_1)

    component_control_implementations_1.implemented_requirements.add(component_implemented_requirements_1)

    # Re-processing model: ssp.models.system_security_plans

    ssp_system_security_plans_1.control_implementation = component_control_implementations_1
    ssp_system_security_plans_1 = importer.save_or_locate(ssp_system_security_plans_1)

    # Re-processing model: component.models.parameters

    # Re-processing model: component.models.statements

    # Re-processing model: component.models.by_components

    # Re-processing model: component.models.implemented_requirements





    # Re-processing model: component.models.control_implementations


