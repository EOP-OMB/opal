from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
import urllib.request
import json
from catalog.models import *


# Create your views here.

class catalog_list_view(ListView):
    model = catalogs
    context_object_name = "catalog_list"


class catalog_detail_view(DetailView):
    model = catalogs
    context_object_name = "catalog"
    template_name = "catalog/catalog_detail.html"


class control_detail_view(DetailView):
    model = controls
    context_object_name = "control"
    template_name = "catalog/control_detail.html"


def import_catalog_view(request, catalog_link):
    """
    Imports a pre-defined set of catalogs
    """
    catalog_dict ={"sp-800-53-r5-high" : "https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_HIGH-baseline-resolved-profile_catalog-min.json",
     "sp-800-53-r5-moderate": "https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_MODERATE-baseline-resolved-profile_catalog-min.json",
     "sp-800-53-r5-low": "https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_LOW-baseline-resolved-profile_catalog-min.json",
     "sp-800-53-r5-privacy": "https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_PRIVACY-baseline-resolved-profile_catalog-min.json",
        }

    if catalog_link in catalog_dict.keys():
        catalog_url = catalog_dict[catalog_link]
        f = urllib.request.urlopen(catalog_url)
        catalog_json = json.loads(f.read().decode('utf-8'))
        catalog_dict = catalog_json["catalog"]
        new_catalog = catalogs()
        new_catalog.import_oscal(catalog_dict)
        new_catalog.save()
        context = {'msg' : new_catalog.metadata.title + " imported from " + catalog_url}
        return render(request, "index.html", context)
    else:
        return "Sorry, we don't know where to get that catalog."
