import requests
import json
import os
import os.path
import urllib
import xmltodict

from django.apps import apps
from django.conf import settings
from django.http import (HttpResponse, HttpResponseRedirect, HttpResponseServerError)
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils

from catalog.models import *
from opal.settings import USER_APPS
from ssp.models import *
from .functions import search_for_uuid, convert_xml_to_json

# Create your views here.

available_catalog_list = [{
    "uuid": "6643738e-4b28-436d-899f-704d88c91f5e", "slug": "nist_sp_800_53_rev_5_high_baseline",
    "name": "NIST SP-800 53 rev5 HIGH baseline",
    "link": "https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_HIGH-baseline-resolved-profile_catalog-min.json"
}, {
    "uuid": "36ade4b6-3e50-4899-b955-9d4a95407c38", "slug": "nist_sp_800_53_rev_5_moderate_baseline",
    "name": "NIST SP-800 53 rev5 MODERATE baseline",
    "link": "https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_MODERATE-baseline-resolved-profile_catalog-min.json"
}, {
    "uuid": "0186ce03-126b-49dd-959f-2fa94059ddd2", "slug": "nist_sp_800_53_rev_5_low_baseline",
    "name": "NIST SP-800 53 rev5 LOW baseline",
    "link": "https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_LOW-baseline-resolved-profile_catalog-min.json"
}, {
    "uuid": "7401e6d3-dec9-4a5b-86dc-309df4519e36", "slug": "nist_sp_800_53_rev_5_privacy_baseline",
    "name": "NIST SP-800 53 rev5 PRIVACY baseline",
    "link": "https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_PRIVACY-baseline-resolved-profile_catalog-min.json"
}, {
    "uuid": "61787e85-adaf-4951-8d16-91f6e0b331bb", "slug": "fed_ramp_rev_4_high_baseline_resolved_profile_catalog",
    "name": "FedRAMP Rev 4 HIGH Baseline",
    "link": "https://raw.githubusercontent.com/GSA/fedramp-automation/master/dist/content/baselines/rev4/json/FedRAMP_rev4_HIGH-baseline-resolved-profile_catalog-min.json"
}, {
    "uuid": "0f9fcab5-995f-412f-8954-49526e1cc80a", "slug": "fed_ramp_rev_4_low_baseline_resolved_profile_catalog_min",
    "name": "FedRAMP Rev 4 LOW Baseline",
    "link": "https://raw.githubusercontent.com/GSA/fedramp-automation/master/dist/content/baselines/rev4/json/FedRAMP_rev4_LOW-baseline-resolved-profile_catalog-min.json"
}, {
    "uuid": "8bf9a86c-66e9-4757-830c-87c0df2fb821",
    "slug": "fed_ramp_rev_4_moderate_baseline_resolved_profile_catalog_min", "name": "FedRAMP Rev 4 MODERATE Baseline",
    "link": "https://raw.githubusercontent.com/GSA/fedramp-automation/master/dist/content/baselines/rev4/json/FedRAMP_rev4_MODERATE-baseline-resolved-profile_catalog-min.json"
}, {
    "uuid": "9a740e35-422f-48e2-baca-0b0c515997d1", "slug": "nist_sp_800_53_rev_4_low",
    "name": "Nist SP 800 53 Rev 4 LOW",
    "link": "https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev4/json/NIST_SP-800-53_rev4_LOW-baseline-resolved-profile_catalog-min.json"
}, {
    "uuid": "be314319-466e-459b-b736-631bd84e3cd7", "slug": "nist_sp_800_53_rev_4_moderate",
    "name": "Nist SP 800 53 Rev 4 MODERATE",
    "link": "https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev4/json/NIST_SP-800-53_rev4_MODERATE-baseline-resolved-profile_catalog-min.json"
}, {
    "uuid": "8f1b188b-5315-4c4d-a95a-1917f3cd5a62", "slug": "nist_sp_800_53_rev_4_high",
    "name": "Nist SP 800 53 Rev 4 High",
    "link": "https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev4/json/NIST_SP-800-53_rev4_HIGH-baseline-resolved-profile_catalog-min.json"
}, ]


@ensure_csrf_cookie
def index_view(request):
    catalog_list_html_str = ""

    for item in available_catalog_list:
        catalog_list_html_str += "<li><a href='"
        catalog_list_html_str += reverse('catalog:import_catalog_view', kwargs={'catalog_link': item['slug']})
        catalog_list_html_str += "'>" + item['name'] + "</a>"
        if catalogs.objects.filter(uuid=item['uuid']).exists():
            catalog_list_html_str += "&#9989;"
        catalog_list_html_str += "</li>"

    ssp_file_str = urllib.parse.quote_plus('ssp-example.json')
    ssp_sample_import_link = reverse('ssp:import_ssp_view', kwargs={'ssp_file': ssp_file_str})

    context = {
        "catalog_list": catalog_list_html_str, "ssp_sample_import_link": ssp_sample_import_link
    }
    # And so on for more models
    return render(request, "index.html", context)


@ensure_csrf_cookie
def authentication_view(request):
    from opal.settings import ENABLE_OIDC, ENABLE_SAML

    html_str = ""
    form_list = []

    if request.user.is_authenticated:
        html_str += "<h2>Welcome %s</h2>" % request.user.get_full_name()
    else:
        if ENABLE_OIDC:
            html_str += "<h2>OIDC Enabled</h2>"
            html_str += "<a href='%s'>Login using OIDC</a>" % settings.OIDC_OP_LOGIN_REDIRECT_URL

        if ENABLE_SAML:
            html_str += "<h2>SAML Enabled</h2>"
            html_str += "<a href='%s'>Login using SAML</a>" % reverse('common:saml_authentication')

    context = {
        "content": html_str, "title": "OPAL Authentication Options"
    }

    return render(request, "generic_template.html", context)


def init_saml_auth(request):
    settings_dict = get_saml_metadata(request)
    saml_settings = OneLogin_Saml2_Settings(settings_dict)
    auth = OneLogin_Saml2_Auth(request, old_settings=settings_dict)
    return auth


# def init_saml_auth(req):
#     auth = OneLogin_Saml2_Auth(req, custom_base_path=settings.SAML_FOLDER)
#     return auth


def prepare_django_request(request):
    # If server is behind proxys or balancers use the HTTP_X_FORWARDED fields
    if 'HTTP_HOST' in request.META:
        http_host = request.META['HTTP_HOST']
    else:
        http_host = request.get_host()
    result = {
        'https': 'on' if request.is_secure() else 'off',
        'http_host': http_host,
        'script_name': request.META['PATH_INFO'], 'get_data': request.GET.copy(),
        # Uncomment if using ADFS as IdP, https://github.com/onelogin/python-saml/pull/144
        # 'lowercase_urlencoding': True,
        'post_data': request.POST.copy()
    }
    logging.info(result)
    return result


def attrs(request):
    paint_logout = False
    attributes = False

    if 'samlUserdata' in request.session:
        paint_logout = True
        if len(request.session['samlUserdata']) > 0:
            attributes = request.session['samlUserdata'].items()
    return render(
        request, 'saml/attrs.html', {
            'paint_logout': paint_logout, 'attributes': attributes
        }
    )


@csrf_exempt
def saml_authentication(request):
    req = prepare_django_request(request)
    auth = init_saml_auth(request)
    errors = []
    error_reason = None
    not_auth_warn = False
    success_slo = False
    attributes = False
    paint_logout = False

    if 'sso' in req['get_data']:
        return HttpResponseRedirect(
            auth.login()
        )  # If AuthNRequest ID need to be stored in order to later validate it, do instead  # sso_built_url = auth.login()  # request.session['AuthNRequestID'] = auth.get_last_request_id()  # return HttpResponseRedirect(sso_built_url)
    elif 'sso2' in req['get_data']:
        return_to = OneLogin_Saml2_Utils.get_self_url(req) + reverse('common:attrs')
        return HttpResponseRedirect(auth.login(return_to))
    elif 'slo' in req['get_data']:
        name_id = session_index = name_id_format = name_id_nq = name_id_spnq = None
        if 'samlNameId' in request.session:
            name_id = request.session['samlNameId']
        if 'samlSessionIndex' in request.session:
            session_index = request.session['samlSessionIndex']
        if 'samlNameIdFormat' in request.session:
            name_id_format = request.session['samlNameIdFormat']
        if 'samlNameIdNameQualifier' in request.session:
            name_id_nq = request.session['samlNameIdNameQualifier']
        if 'samlNameIdSPNameQualifier' in request.session:
            name_id_spnq = request.session['samlNameIdSPNameQualifier']

        return HttpResponseRedirect(
            auth.logout(
                name_id=name_id, session_index=session_index, nq=name_id_nq, name_id_format=name_id_format,
                spnq=name_id_spnq
            )
        )  # If LogoutRequest ID need to be stored in order to later validate it, do instead  # slo_built_url = auth.logout(name_id=name_id, session_index=session_index)  # request.session['LogoutRequestID'] = auth.get_last_request_id()  # return HttpResponseRedirect(slo_built_url)
    elif 'acs' in req['get_data']:
        request_id = None
        if 'AuthNRequestID' in request.session:
            request_id = request.session['AuthNRequestID']

        auth.process_response(request_id=request_id)
        errors = auth.get_errors()
        not_auth_warn = not auth.is_authenticated()

        if not errors:
            if 'AuthNRequestID' in request.session:
                del request.session['AuthNRequestID']
            request.session['samlUserdata'] = auth.get_attributes()
            request.session['samlNameId'] = auth.get_nameid()
            request.session['samlNameIdFormat'] = auth.get_nameid_format()
            request.session['samlNameIdNameQualifier'] = auth.get_nameid_nq()
            request.session['samlNameIdSPNameQualifier'] = auth.get_nameid_spnq()
            request.session['samlSessionIndex'] = auth.get_session_index()
            if 'RelayState' in req['post_data'] and OneLogin_Saml2_Utils.get_self_url(req) != req['post_data'][
                'RelayState']:
                # To avoid 'Open Redirect' attacks, before execute the redirection confirm
                # the value of the req['post_data']['RelayState'] is a trusted URL.
                return HttpResponseRedirect(auth.redirect_to(req['post_data']['RelayState']))
        elif auth.get_settings().is_debug_active():
            error_reason = auth.get_last_error_reason()
    elif 'sls' in req['get_data']:
        request_id = None
        if 'LogoutRequestID' in request.session:
            request_id = request.session['LogoutRequestID']
        dscb = lambda: request.session.flush()
        url = auth.process_slo(request_id=request_id, delete_session_cb=dscb)
        errors = auth.get_errors()
        if len(errors) == 0:
            if url is not None:
                # To avoid 'Open Redirect' attacks, before execute the redirection confirm
                # the value of the url is a trusted URL
                return HttpResponseRedirect(url)
            else:
                success_slo = True
        elif auth.get_settings().is_debug_active():
            error_reason = auth.get_last_error_reason()

    if 'samlUserdata' in request.session:
        paint_logout = True
        if len(request.session['samlUserdata']) > 0:
            attributes = request.session['samlUserdata'].items()

    return render(
        request, 'saml/saml_authentication.html', {
            'errors': errors, 'error_reason': error_reason, 'not_auth_warn': not_auth_warn, 'success_slo': success_slo,
            'attributes': attributes, 'paint_logout': paint_logout
        }
    )


def metadata(request):
    # req = prepare_django_request(request)
    # auth = init_saml_auth(req)
    # saml_settings = auth.get_settings()

    settings_dict = get_saml_metadata(request)

    saml_settings = OneLogin_Saml2_Settings(
        settings=settings_dict, sp_validation_only=True
    )
    metadata_xml = saml_settings.get_sp_metadata()
    errors = saml_settings.validate_metadata(metadata_xml)

    if len(errors) == 0:
        resp = HttpResponse(content=metadata_xml, content_type='text/xml')
    else:
        resp = HttpResponseServerError(content=', '.join(errors))
    return resp


def get_saml_metadata(request):
    filename = os.path.join(settings.SAML_FOLDER, settings.SAML_SETTINGS_JSON)
    if request.is_secure():
        host_name = "https://"
    else:
        host_name = "http://"
    host_name += request.get_host() + "/"
    logging.info("Got host: " + host_name)
    with open(filename, 'r') as json_data:
        settings_dict = json.loads(json_data.read())
    settings_dict['sp']['entityId'] = host_name + '/common/saml/metadata'
    settings_dict['sp']['assertionConsumerService']['url'] = host_name + '/common/saml/?acs'
    settings_dict['sp']['singleLogoutService']['url'] = host_name + '/common/saml/?sls'
    if settings.SAML_TECHNICAL_POC:
        settings_dict['contactPerson'] = {
            'technical': {'givenName': settings.SAML_TECHNICAL_POC, 'emailAddress': settings.SAML_TECHNICAL_POC_EMAIL}
        }
    if settings.SAML_TECHNICAL_POC:
        settings_dict['contactPerson'] = {
            'support': {'givenName': settings.SAML_SUPPORT_POC, 'emailAddress': settings.SAML_SUPPORT_POC_EMAIL}
        }
    settings_dict['organization']['en-US']['url'] = host_name

    # Add IDP sections
    proxies = {}
    if settings.HTTP_PROXY:
        proxies['http'] = settings.HTTP_PROXY
    if settings.HTTPS_PROXY:
        proxies['https'] = settings.HTTPS_PROXY

    max_idp_metadata = requests.get('https://login.max.gov/idp/shibboleth', proxies=proxies).text

    import xml.etree.ElementTree as ET

    root = ET.fromstring(max_idp_metadata)

    ns = {
        "": "urn:oasis:names:tc:SAML:2.0:metadata",
        "ds": "http://www.w3.org/2000/09/xmldsig#",
        "shibmd": "urn:mace:shibboleth:metadata:1.0",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance"
    }

    settings_dict['idp'] = {
        "entityId": root.attrib['entityID'],
        "x509cert": root.find(".//ds:X509Certificate", ns).text
    }

    for e in root[0].findall("{urn:oasis:names:tc:SAML:2.0:metadata}SingleSignOnService"):
        if e.attrib['Binding'] == 'urn:mace:shibboleth:1.0:profiles:AuthnRequest':
            settings_dict['idp']["singleSignOnService"] = {"binding": e.attrib['Binding'], "url": e.attrib['Location']}

    # idp_dict = xmltodict.parse(max_idp_metadata)['EntityDescriptor']
    #
    # settings_dict['idp'] = {
    #     "entityId": idp_dict['@entityID'],
    #     "singleSignOnService": {
    #         "url": "https://app.onelogin.com/trust/saml2/http-post/sso/<onelogin_connector_id>",
    #         "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
    #     },
    #     "singleLogoutService": {
    #         "url": "https://app.onelogin.com/trust/saml2/http-redirect/slo/<onelogin_connector_id>",
    #         "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
    #     },
    #     "x509cert": "<onelogin_connector_cert>"
    # }

    return settings_dict


def database_status_view(request):
    model_list = []
    for a in USER_APPS:
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
    except AttributeError as e:
        err_msg = e
    return redirect(to=redirect_url)


def error_404_view(request, exception):
    template_name = "404.html"
    context_object_name = "obj"
