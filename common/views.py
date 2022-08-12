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
        "ssp_sample_import_link": ssp_sample_import_link
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