import urllib

from django.apps import apps
from django.shortcuts import redirect, render

from catalog.models import *
from opal.settings import USER_APPS
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
    }]


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
        "ssp_sample_import_link" : ssp_sample_import_link
        }
    # And so on for more models
    return render(request, "index.html", context)


def DatabaseStatusView(request):
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
