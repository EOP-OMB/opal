import os
import urllib
import uuid
from io import StringIO

from django import forms
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django_require_login.decorators import public
from django.conf import settings
import base64 as b64

from catalog.models import available_catalog_list
from common.forms import resource_form, UploadFileForm, props_form, links_form
from common.functions import search_for_uuid
from common.models import base64


def index_view(request):
    if User.is_staff:
        catalog_list_html_str = ""

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
    else:
        return render(request, "base.html")


def auth_view(request):
    return render(request, "auth.html")


def error_404_view(request, exception):
    context = {"exception": exception}
    return render(request,"404.html", context)


if settings.ENABLE_SAML == 'True':
    from sp.models import IdP
    from sp.utils import get_session_idp
    @public
    def auth_view(request):
        if request.headers.get('Referer'):
            next_page = request.headers.get('Referer')
        else:
            next_page = '/'
        context = {"idp": get_session_idp(request),
                   "idps": IdP.objects.filter(is_active=True),
                   "enable_django_auth": bool(settings.ENABLE_DJANGO_AUTH),
                   "next": next_page
                   }
        return render(request, "auth.html", context)


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


def permalink_view(p_uuid):
    obj = search_for_uuid(p_uuid)
    try:
        redirect_url = obj.get_absolute_url()
        return redirect(redirect_url)
    except AttributeError:
        err_msg = "No object with that UUID was found"
        return HttpResponseNotFound(err_msg)


class base64_list_view(ListView):
    model = base64
    context_object_name = "context_list"
    template_name = "generic_list.html"
    add_new_url = reverse_lazy('common:upload_file')
    extra_context = {
        'add_url': add_new_url,
        'title': 'Files',
    }


def base64_detail_view(request, pk):
    base64_object = base64.objects.get(pk=pk)
    file_url = base64_object.render_file()
    html_str = "<h1>%s</h1>" % base64_object.filename
    html_str += "<img src='%s'>" % file_url
    html_str += "<hr>"
    html_str += "<a href='%s'>Download File</a>" % file_url
    return render(request, "generic_template.html", {'content': html_str})


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form_filename = request.POST['title']
            form_file_binary = request.FILES["file"]
            form_media_type = form_file_binary.content_type
            file_binary = form_file_binary.read()
            file_base64 = (b64.b64encode(file_binary)).decode('ascii')
            new_attachment, _ = base64.objects.get_or_create(
                filename=form_filename,
                media_type=form_media_type,
                value=file_base64
            )
            new_attachment.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('common:base64_detail', args=(new_attachment.pk,)))
    else:
        form = UploadFileForm()
    return render(request, "generic_form.html", {"form": form})


def add_resource_view(request):
    if request.method == "POST":
        form = resource_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'generic_template.html', {
                'title': "Resource added",
                'content': "You may close this window"
            })
    else:
        return render(
            request, 'generic_form.html', {
                'title': 'Add a new Document',
                'content': "All fields are required",
                'form': resource_form
            })


def download_oscal_json(j):

    oscal_jason_file = open('%s.json' % uuid.uuid4(), 'x')
    oscal_jason_file.write(j)
    path_to_file = os.path.realpath(oscal_jason_file)
    response = FileResponse(open(path_to_file, 'rb'))
    file_name = oscal_jason_file[5:]
    response['Content-Disposition'] = 'inline; filename=' + file_name
    return response
