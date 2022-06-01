import urllib
from django.conf import settings
from django.apps import apps
from django.shortcuts import redirect, render
from catalog.models import *
from ssp.models import *
from .functions import search_for_uuid

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
        "catalog_list": catalog_list_html_str,
        "ssp_sample_import_link": ssp_sample_import_link
        }
    # And so on for more models
    return render(request, "index.html", context)


def login(request):
    auth_list_html_str = "<ul>"

    auth_list_html_str += "</ul>"

    context = {
        "title": 'OPAL Authentication Options',
        "content": auth_list_html_str
        }


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
    except AttributeError as e:
        err_msg = e
    return redirect(to=redirect_url)


def error_404_view(request, exception):
    template_name = "404.html"
    context_object_name = "obj"
    return render(request, "404.html", exception)
