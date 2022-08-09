from ntpath import join
import urllib
from django.http import HttpResponseNotFound
from django.contrib.auth import get_user_model
from django.conf import settings
from django.apps import apps
from django.shortcuts import redirect, render
from django.urls import reverse
from sp.models import IdP
from sp.utils import get_session_idp

from catalog.models import available_catalog_list, catalogs
from common.models import roles
from catalog.views import download_catalog
from .functions import search_for_uuid


# Create your views here.


def index_view(request):
    User = get_user_model()

    catalog_list_html_str = ""
    catalog_imported = ""

    for item in available_catalog_list.objects.all():
        catalog_list_html_str += item.get_link()

    ssp_file_str = urllib.parse.quote_plus('ssp-example.json')
    ssp_sample_import_link = reverse('ssp:import_ssp_view', kwargs={'ssp_file': ssp_file_str})

    context = {
        "catalog_list": catalog_list_html_str,
        "ssp_sample_import_link": ssp_sample_import_link,
        "app_initialized": User.objects.filter(is_superuser=True).exists()
        }
    # And so on for more models
    return render(request, "index.html", context)


def auth_view(request):
    context = {"idp": get_session_idp(request), "idps": IdP.objects.filter(is_active=True)}
    return render (request, "auth.html", context)



def database_status_view(request):
    model_list = []
    for a in settings.USER_APPS:
        app_models = apps.get_app_config(a).get_models()
        for m in app_models:
            if m.objects.count() > 0:
                s = m.__name__ + ":" + str(m.objects.count())
                model_list.append(s)
    model_list.sort()
    context = {"model_list": model_list}
    return render(request, "db_status.html", context)


def permalink(request, p_uuid):
    redirect_url = "error_404_view"
    obj = search_for_uuid(p_uuid)
    try:
        redirect_url = obj.get_absolute_url()
        return redirect(redirect_url)
    except AttributeError as e:
        err_msg = "No object with that UUID was found"
        return HttpResponseNotFound(err_msg)


def app_init(request):

    content = []

    # If no admin user exists, create an admin account
    user = get_user_model()
    if not user.objects.filter(is_superuser=True).exists():
        password = create_admin_user(user)
        content.append("Created account 'admin' with password '%s'. This password will not be displayed again." % password)

    # Populate the Catalog import list
    catalog_list = load_catalog_import_list()

    content.append("Added %s entries to the available catalog list" % len(catalog_list))

    # Add some default roles
    default_role_list = load_default_role_list()

    content.append("Added %s default roles" % len(default_role_list))

    return render(request, "generic_template.html", {'title': "Bootstrap Tasks Completed", 'content': '<hr>'.join(content)})


def load_default_role_list():
    default_role_list = [
        {
            "role_id": "AO",
            "title": "Authorizing Official",
            "short_name": "AO",
            "description": "The authorizing official is a senior official or executive with the authority to formally assume responsibility and accountability for operating a system; providing common controls inherited by organizational systems; or using a system, service, or application from an external provider. The authorizing official is the only organizational official who can accept the security and privacy risk to organizational operations, organizational assets, and individuals.115 Authorizing officials typically have budgetary oversight for the system or are responsible for the mission and/or business operations supported by the system. Accordingly, authorizing officials are in management positions with a level of authority commensurate with understanding and accepting such security and privacy risks. Authorizing officials approve plans, memorandums of agreement or understanding, plans of action and milestones, and determine whether significant changes in the information systems or environments of operation require reauthorization.\r\nAuthorizing officials coordinate their activities with common control providers, system owners, chief information officers, senior agency information security officers, senior agency officials for privacy, system security and privacy officers, control assessors, senior accountable officials for risk management/risk executive (function), and other interested parties during the authorization process. With the increasing complexity of the mission/business processes in an organization, partnership arrangements, and the use of shared services, it is possible that a system may involve co-authorizing officials. If so, agreements are established between the co-authorizing officials and documented in the security and privacy plans. Authorizing officials are responsible and accountable for ensuring that authorization activities and functions that are delegated to authorizing official designated representatives are carried out as specified. For federal agencies, the role of authorizing official is an inherent U.S. Government function and is assigned to government personnel only."
            },
        {
            "role_id": "AODR",
            "title": "Authorizing Official Designated Representative",
            "short_name": "AODR",
            "description": "The authorizing official designated representative is an organizational official designated by the authorizing official who is empowered to act on behalf of the authorizing official to coordinate and conduct the day-to-day activities associated with managing risk to information systems and organizations. This includes carrying out many of the activities related to the execution of the RMF. The only activity that cannot be delegated by the authorizing official to the designated representative is the authorization decision and signing of the associated authorization decision document (i.e., the acceptance of risk)."
            },
        {
            "role_id": "CAO",
            "title": "Chief Acquisition Officer",
            "short_name": "CAO",
            "description": "The chief acquisition officer is an organizational official designated by the head of an agency to advise and assist the head of agency and other agency officials to ensure that the mission of the agency is achieved through the management of the agency’s acquisition activities. The chief acquisition officer monitors the performance of acquisition activities and programs; establishes clear lines of authority, accountability, and responsibility for acquisition decision making within the agency; manages the direction and implementation of acquisition policy for the agency; and establishes policies, procedures, and practices that promote full and open competition from responsible sources to fulfill best value requirements considering the nature of the property or service procured. The Chief Acquisition Officer coordinates with mission or business owners, authorizing officials, senior accountable official for risk management, system owners, common control providers, senior agency information security officer, senior agency official for privacy, and risk executive (function) to ensure that security and privacy requirements are defined in organizational procurements and acquisitions."
            },
        {
            "role_id": "CIO",
            "title": "Chief Information Officer",
            "short_name": "CIO",
            "description": "The chief information officer is an organizational official responsible for designating a senior agency information security officer; developing and maintaining security policies, procedures, and control techniques to address security requirements; overseeing personnel with significant responsibilities for security and ensuring that the personnel are adequately trained; assisting senior organizational officials concerning their security responsibilities; and reporting to the head of the agency on the effectiveness of the organization’s security program, including progress of remedial actions. The chief information officer, with the support of the senior accountable official for risk management, the risk executive (function), and the senior agency information security officer, works closely with authorizing officials and their designated representatives to help ensure that:\r\n• An organization-wide security program is effectively implemented resulting in adequate security for all organizational systems and environments of operation;\r\n• Security and privacy (including supply chain) risk management considerations are integrated into programming/planning/budgeting cycles, enterprise architectures, the SDLC, and acquisitions;\r\n• Organizational systems and common controls are covered by approved system security plans and possess current authorizations;\r\n• Security activities required across the organization are accomplished in an efficient, cost- effective, and timely manner; and\r\n• There is centralized reporting of security activities.\r\nThe chief information officer and authorizing officials determine the allocation of resources dedicated to the protection of systems supporting the organization’s missions and business functions based on organizational priorities. For information systems that process personally identifiable information, the chief information officer and authorizing officials coordinate any determination about the allocation of resources dedicated to the protection of those systems with the senior agency official for privacy. For selected systems, the chief information officer may be designated as an authorizing official or a co-authorizing official with other senior organizational officials. The role of chief information officer is an inherent U.S. Government function and is assigned to government personnel only."
            },
        {
            "role_id": "CA",
            "title": "Control Assessor",
            "short_name": "CA",
            "description": "The control assessor is an individual, group, or organization responsible for conducting a comprehensive assessment of implemented controls and control enhancements to determine the effectiveness of the controls (i.e., the extent to which the controls are implemented correctly, operating as intended, and producing the desired outcome with respect to meeting the security and privacy requirements for the system and the organization). For systems, implemented system-specific controls and system-implemented parts of hybrid controls are assessed. For common controls, implemented common controls and common control- implemented parts of hybrid controls are assessed. The system owner and common control provider rely on the security and privacy expertise and judgment of the assessor to assess the implemented controls using the assessment procedures specified in the security and privacy assessment plans. Multiple control assessors who are differentiated by their expertise in specific control requirements or technologies may be required to conduct the assessment effectively. Prior to initiating the control assessment, assessors review the security and privacy plans to facilitate development of the assessment plans. Control assessors provide an assessment of the severity of the deficiencies discovered in the system, environment of operation, and common controls and can recommend corrective actions to address the identified vulnerabilities. For system-level control assessments, control assessors do not assess inherited controls, and only assess the system-implemented portions of hybrid controls. Control assessors prepare security and privacy assessment reports containing the results and findings from the assessment.\r\nThe required level of assessor independence is determined by the authorizing official based on laws, executive orders, directives, regulations, policies, standards, or guidelines. When a control assessment is conducted in support of an authorization decision or ongoing authorization, the authorizing official makes an explicit determination of the degree of independence required. Assessor independence is a factor in preserving an impartial and unbiased assessment process; determining the credibility of the assessment results; and ensuring that the authorizing official receives objective information to make an informed, risk-based authorization decision.\r\nThe senior agency official for privacy is responsible for assessing privacy controls and for providing privacy information to the authorizing official. At the discretion of the organization, privacy controls may be assessed by an independent assessor. However, in all cases, the senior agency official for privacy retains responsibility and accountability for the privacy program of the organization, including any privacy functions performed by the independent assessors."
            },
        {
            "role_id": "EA",
            "title": "Enterprise Architect",
            "short_name": "EA",
            "description": "The enterprise architect is an individual or group responsible for working with the leadership and subject matter experts in an organization to build a holistic view of the organization's missions and business functions, mission/business processes, information, and information technology assets. With respect to information security and privacy, enterprise architects:\r\n• Implement an enterprise architecture strategy that facilitates effective security and privacy solutions;\r\n• Coordinate with security and privacy architects to determine the optimal placement of systems/system elements within the enterprise architecture and to address security and privacy issues between systems and the enterprise architecture;\r\n• Assist in reducing complexity within the IT infrastructure to facilitate security;\r\n• Assist with determining appropriate control implementations and initial configuration\r\nbaselines as they relate to the enterprise architecture;\r\n• Collaborate with system owners and authorizing officials to facilitate authorization boundary determinations and allocation of controls to system elements;\r\n• Serve as part of the Risk Executive (function); and\r\n• Assist with integration of the organizational risk management strategy and system-level security and privacy requirements into program, planning, and budgeting activities, the SDLC, acquisition processes, security and privacy (including supply chain) risk management, and systems engineering processes."
            },
        {
            "role_id": "HOA",
            "title": "Head Of Agency",
            "short_name": "HOA",
            "description": "The head of agency is responsible and accountable for providing information security protections commensurate with the risk to organizational operations and assets, individuals, other organizations, and the Nation—that is, risk resulting from unauthorized access, use, disclosure, disruption, modification, or destruction of information collected or maintained by or on behalf of the agency; and the information systems used or operated by an agency or by a contractor of an agency or other organization on behalf of an agency. The head of agency is also the senior official in an organization with the responsibility for ensuring that privacy interests are protected and that PII is managed responsibly within the organization. The heads of agencies ensure that:\r\n• Information security and privacy management processes are integrated with strategic and operational planning processes;\r\n• Senior officials within the organization provide information security for the information and systems supporting the operations and assets under their control;\r\n• Senior agency officials for privacy are designated who are responsible and accountable for ensuring compliance with applicable privacy requirements, managing privacy risk, and the organization’s privacy program; and\r\n• The organization has adequately trained personnel to assist in complying with security and privacy requirements in legislation, executive orders, policies, directives, instructions, standards, and guidelines.\r\nThe head of agency establishes the organizational commitment and the actions required to effectively manage security and privacy risk and protect the missions and business functions being carried out by the organization. The head of agency establishes security and privacy accountability and provides active support and oversight of monitoring and improvement for the security and privacy programs. Senior leadership commitment to security and privacy establishes a level of due diligence within the organization that promotes a climate for mission and business success."
            },
        {
            "role_id": "IO",
            "title": "Information Owner",
            "short_name": "IO",
            "description": "The information owner or steward is an organizational official with statutory, management, or operational authority for specified information and the responsibility for establishing the policies and procedures governing its generation, collection, processing, dissemination, and disposal. In information-sharing environments, the information owner/steward is responsible for establishing the rules for appropriate use and protection of the information and retains that responsibility even when the information is shared with or provided to other organizations. The owner/steward of the information processed, stored, or transmitted by a system may or may not be the same individual as the system owner. An individual system may contain information from multiple information owners/stewards. Information owners/stewards provide input to system owners regarding the security and privacy requirements and controls for the systems where the information is processed, stored, or transmitted."
            },
        {
            "role_id": "MO",
            "title": "Mission Owner",
            "short_name": "MO",
            "description": "The mission or business owner is the senior official or executive within an organization with specific mission or line of business responsibilities and that has a security or privacy interest in the organizational systems supporting those missions or lines of business. Mission or business owners are key stakeholders that have a significant role in establishing organizational mission and business processes and the protection needs and security and privacy requirements that ensure the successful conduct of the organization’s missions and business operations. Mission and business owners provide essential inputs to the risk management strategy, play an active part in the SDLC, and may also serve in the role of authorizing official.",
            },
        {
            "role_id": "SAORM",
            "title": "Senior Accountable Official For Risk Management",
            "short_name": "SAORM",
            "description": "The senior accountable official for risk management is the individual that leads and manages the risk executive (function) in an organization and is responsible for aligning information security and privacy risk management processes with strategic, operational, and budgetary planning processes. The senior accountable official for risk management is the head of the agency or an individual designated by the head of the agency. The senior accountable official for risk management determines the organizational structure and responsibilities of the risk executive (function), and in coordination with the head of the agency, may retain the risk executive (function) or delegate the function to another organizational official or group. The senior accountable official for risk management is an inherent U.S. Government function and is assigned to government personnel only."
            },
        {
            "role_id": "CISO",
            "title": "Senior Agency Information Security Officer",
            "short_name": "CISO",
            "description": "The senior agency information security officer is an organizational official responsible for carrying out the chief information officer security responsibilities under FISMA, and serving as the primary liaison for the chief information officer to the organization’s authorizing officials, system owners, common control providers, and system security officers. The senior agency information security officer is also responsible for coordinating with the senior agency official for privacy to ensure coordination between privacy and information security programs. The senior agency information security officer possesses the professional qualifications, including training and experience, required to administer security program functions; maintains security duties as a primary responsibility; and heads an office with the specific mission and resources to assist the organization in achieving trustworthy, secure information and systems in accordance with the requirements in FISMA. The senior agency information security officer may serve as authorizing official designated representative or as a security control assessor. The role of senior agency information security officer is an inherent U.S. Government function and is therefore assigned to government personnel only. Organizations may also refer to the senior agency information security officer as the senior information security officer or chief information security officer."
            },
        {
            "role_id": "SAOP",
            "title": "Senior Agency Official For Privacy",
            "short_name": "SAOP",
            "description": "The senior agency official for privacy is the senior official or executive with agency-wide responsibility and accountability for ensuring compliance with applicable privacy requirements and managing privacy risk. Among other things, the senior agency official for privacy is responsible for:\r\n• Coordinating with the senior agency information security officer to ensure coordination of privacy and information security activities;\r\n• Reviewing and approving the categorization of information systems that create, collect, use, process, store, maintain, disseminate, disclose, or dispose of personally identifiable information;\r\n• Designating which privacy controls will be treated as program management, common, system-specific, and hybrid privacy controls;\r\n• Identifying assessment methodologies and metrics to determine whether privacy controls are implemented correctly, operating as intended, and sufficient to ensure compliance with applicable privacy requirements and manage privacy risks;\r\n• Reviewing and approving privacy plans for information systems prior to authorization, reauthorization, or ongoing authorization;\r\n• Reviewing authorization packages for information systems that create, collect, use, process, store, maintain, disseminate, disclose, or dispose of personally identifiable information to ensure compliance with privacy requirements and manage privacy risks;\r\n• Conducting and documenting the results of privacy control assessments to verify the continued effectiveness of all privacy controls selected and implemented at the agency; and\r\n• Establishing and maintaining a privacy continuous monitoring program to maintain ongoing awareness of privacy risks and assess privacy controls at a frequency sufficient to ensure compliance with privacy requirements and manage privacy risks.\r\nThe role of senior agency official for privacy is an inherent U.S. Government function and is therefore assigned to government personnel only."
            },
        {
            "role_id": "SA",
            "title": "System Administrator",
            "short_name": "SA",
            "description": "The system administrator is an individual, group, or organization responsible for setting up and maintaining a system or specific system elements. System administrator responsibilities include, for example, installing, configuring, and updating hardware and software; establishing and managing user accounts; overseeing or conducting backup, recovery, and reconstitution activities; implementing controls; and adhering to and enforcing organizational security and privacy policies and procedures. The system administrator role includes other types of system administrators (e.g., database administrators, network administrators, web administrators, and application administrators)."
            },
        {
            "role_id": "SO",
            "title": "System Owner",
            "short_name": "SO",
            "description": "The system owner is an organizational official responsible for the procurement, development, integration, modification, operation, maintenance, and disposal of a system.121 The system owner is responsible for addressing the operational interests of the user community (i.e., users who require access to the system to satisfy mission, business, or operational requirements) and for ensuring compliance with security requirements. In coordination with the system security and privacy officers, the system owner is responsible for the development and maintenance of the security and privacy plans and ensures that the system is operated in accordance with the selected and implemented controls.\r\nIn coordination with the information owner/steward, the system owner decides who has access to the system (and with what types of privileges or access rights).122 The system owner ensures that system users and support personnel receive the requisite security and privacy training. Based on guidance from the authorizing official, the system owner informs organizational officials of the need to conduct the authorization, ensures that resources are available for the effort, and provides the required system access, information, and documentation to control assessors. The system owner receives the security and privacy assessment results from the control assessors. After taking appropriate steps to reduce or eliminate vulnerabilities or security and privacy risks, the system owner assembles the authorization package and submits the package to the authorizing official or the authorizing official designated representative for adjudication."
            },
        {
            "role_id": "SSO",
            "title": "System Security Officer",
            "short_name": "SSO",
            "description": "The system security or privacy officer124 is an individual responsible for ensuring that the security and privacy posture is maintained for an organizational system and works in close collaboration with the system owner. The system security or privacy officer also serves as a principal advisor on all matters, technical and otherwise, involving the controls for the system. The system security or privacy officer has the knowledge and expertise to manage the security or privacy aspects of an organizational system and, in many organizations, is assigned responsibility for the day-to-day system security or privacy operations. This responsibility may also include, but is not limited to, physical and environmental protection; personnel security; incident handling; and security and privacy training and awareness.\r\nThe system security or privacy officer may be called on to assist in the development of the system-level security and privacy policies and procedures and to ensure compliance with those policies and procedures. In close coordination with the system owner, the system security or privacy officer often plays an active role in the monitoring of a system and its environment of operation to include developing and updating security and privacy plans, managing and controlling changes to the system, and assessing the security or privacy impact of those changes.\r\nWhen the system security officer and system privacy officer are separate roles, the system security officer is generally responsible for aspects of the system that protect information and information systems from unauthorized system activity or behavior to provide confidentiality, integrity, and availability. The system privacy officer is responsible for aspects of the system that ensure compliance with privacy requirements and manage the privacy risks to individuals associated with the processing of PII. The responsibilities of system security officers and system privacy officers overlap regarding aspects of the system that protect the security of PII."
            },
        {
            "role_id": "SPO",
            "title": "System Privacy Officer",
            "short_name": "SPO",
            "description": "The system security or privacy officer124 is an individual responsible for ensuring that the security and privacy posture is maintained for an organizational system and works in close collaboration with the system owner. The system security or privacy officer also serves as a principal advisor on all matters, technical and otherwise, involving the controls for the system. The system security or privacy officer has the knowledge and expertise to manage the security or privacy aspects of an organizational system and, in many organizations, is assigned responsibility for the day-to-day system security or privacy operations. This responsibility may also include, but is not limited to, physical and environmental protection; personnel security; incident handling; and security and privacy training and awareness.\r\nThe system security or privacy officer may be called on to assist in the development of the system-level security and privacy policies and procedures and to ensure compliance with those policies and procedures. In close coordination with the system owner, the system security or privacy officer often plays an active role in the monitoring of a system and its environment of operation to include developing and updating security and privacy plans, managing and controlling changes to the system, and assessing the security or privacy impact of those changes.\r\nWhen the system security officer and system privacy officer are separate roles, the system security officer is generally responsible for aspects of the system that protect information and information systems from unauthorized system activity or behavior to provide confidentiality, integrity, and availability. The system privacy officer is responsible for aspects of the system that ensure compliance with privacy requirements and manage the privacy risks to individuals associated with the processing of PII. The responsibilities of system security officers and system privacy officers overlap regarding aspects of the system that protect the security of PII."
            },
        {
            "role_id": "USER",
            "title": "System User",
            "short_name": "USER",
            "description": "The system user is an individual or (system) process acting on behalf of an individual that is authorized to access information and information systems to perform assigned duties. System user responsibilities include, but are not limited to, adhering to organizational policies that govern acceptable use of organizational systems; using the organization-provided information technology resources for defined purposes only; and reporting anomalous or suspicious system behavior."
            },
        {
            "role_id": "SSE",
            "title": "Systems Security Or Privacy Engineer",
            "short_name": "SSE",
            "description": "The systems security or privacy engineer is an individual, group, or organization responsible for conducting systems security or privacy engineering activities as part of the SDLC. Systems security and privacy engineering is a process that captures and refines security and privacy requirements for systems and ensures that the requirements are effectively integrated into systems and system elements through security or privacy architecting, design, development, and configuration. Systems security or privacy engineers are part of the development team— designing and developing organizational systems or upgrading existing systems along with ensuring continuous monitoring requirements are addressed at the system level. Systems security or privacy engineers employ best practices when implementing controls including software engineering methodologies; system and security or privacy engineering principles; secure or privacy-enhancing design, secure or privacy-enhancing architecture, and secure or privacy-enhancing coding techniques. Systems security or privacy engineers coordinate security and privacy activities with senior agency information security officers, senior agency officials for privacy, security and privacy architects, system owners, common control providers, and system security or privacy officers.\r\nWhen the systems security engineer and privacy engineer are separate roles, the systems security engineer is generally responsible for those activities associated with protecting information and information systems from unauthorized system activity or behavior to provide confidentiality, integrity, and availability. The privacy engineer is responsible for those activities associated with ensuring compliance with privacy requirements and managing the privacy risks to individuals associated with the processing of PII. The responsibilities of systems security engineers and privacy engineers overlap regarding activities associated with protecting the security of PII."
            }
        ]
    for role in default_role_list:
        roles.objects.get_or_create(**role)
    return default_role_list


def load_catalog_import_list():
    catalog_list = ['https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_HIGH-baseline-resolved-profile_catalog-min.json',
                    'https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_MODERATE-baseline-resolved-profile_catalog-min.json',
                    'https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_LOW-baseline-resolved-profile_catalog-min.json',
                    'https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_PRIVACY-baseline-resolved-profile_catalog-min.json',
                    'https://raw.githubusercontent.com/GSA/fedramp-automation/master/dist/content/baselines/rev4/json/FedRAMP_rev4_HIGH-baseline-resolved-profile_catalog-min.json',
                    'https://raw.githubusercontent.com/GSA/fedramp-automation/master/dist/content/baselines/rev4/json/FedRAMP_rev4_LOW-baseline-resolved-profile_catalog-min.json',
                    'https://raw.githubusercontent.com/GSA/fedramp-automation/master/dist/content/baselines/rev4/json/FedRAMP_rev4_MODERATE-baseline-resolved-profile_catalog-min.json',
                    'https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev4/json/NIST_SP-800-53_rev4_LOW-baseline-resolved-profile_catalog-min.json',
                    'https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev4/json/NIST_SP-800-53_rev4_MODERATE-baseline-resolved-profile_catalog-min.json',
                    'https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev4/json/NIST_SP-800-53_rev4_HIGH-baseline-resolved-profile_catalog-min.json']
    for c in catalog_list:
        catalog_dict = download_catalog(c)
        available_catalog_list_item = {
            'catalog_uuid': catalog_dict['uuid'],
            'name': catalog_dict['metadata']['title'],
            'link': c,
            }
        available_catalog_list.objects.get_or_create(**available_catalog_list_item)
    return catalog_list


def create_admin_user(user):
    password = user.objects.make_random_password()
    user.objects.create_superuser(
        "admin",
        "",
        password,
        first_name="Admin",
        last_name="User",
        )
    return password
