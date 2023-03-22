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
from sp.models import IdP
from sp.utils import get_session_idp

from catalog.models import available_catalog_list
from common.forms import resource_form
from common.functions import search_for_uuid
from common.models import base64


# Create your views here.


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


@public
def auth_view(request):
    context = {"idp": get_session_idp(request),
               "idps": IdP.objects.filter(is_active=True),
               # "enable_django_auth": bool(settings.ENABLE_DJANGO_AUTH)
               "enable_django_auth": bool(settings.ENABLE_DJANGO_AUTH)
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


def permalink_view(request, p_uuid):
    redirect_url = "error_404_view"
    obj = search_for_uuid(p_uuid)
    try:
        redirect_url = obj.get_absolute_url()
        return redirect(redirect_url)
    except AttributeError:
        err_msg = "No object with that UUID was found"
        return HttpResponseNotFound(err_msg)


class attachment_form(forms.ModelForm):
    filename = forms.CharField(max_length=1000, required=True)
    media_type = forms.CharField(max_length=1000, required=True)
    value = forms.FileField()

    class Meta:
        model = base64
        fields = 'filename', 'media_type', 'value'


def add_base64_attachment_view(request):
    add_new_url = reverse_lazy('common:add_base64_attachment_view')
    if request.POST:
        try:
            form_filename = request.POST['filename']
            form_media_type = request.POST['media_type']
            form_file_binary = request.POST['value']
        except (KeyError, ObjectDoesNotExist):
            # Redisplay the question voting form.
            return render(
                request, 'generic_form.html', {
                    'add_url': add_new_url,
                    'title': 'Upload a new file',
                    'content': "Something went wrong",
                    'form': attachment_form
                }
            )
        else:
            file_base64 = StringIO(form_file_binary)
            new_attachment, created = base64.objects.get_or_create(
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
        return render(
            request, 'generic_form.html', {
                'add_url': add_new_url,
                'title': 'Add a new Document',
                'content': "All fields are required",
                'form': attachment_form()
            }
        )


class base64_list_view(ListView):
    model = base64
    context_object_name = "context_list"
    template_name = "generic_list.html"
    add_new_url = reverse_lazy('common:create_base64')
    extra_context = {
        'add_url': add_new_url,
        'title': 'Files',
    }


class base64_detail_view(DetailView):
    model = base64
    context_object_name = "context"
    template_name = "common/base64_detail.html"


def base64_render_view(request, pk):
    file = base64.objects.get(pk=pk)
    return file.render_file()


def add_resource_view(request):
    return render(
            request, 'generic_form.html', {
                'title': 'Add a new Document',
                'content': "All fields are required",
                'form': resource_form
            })


def download_oscal_json(request, j):

    file = open('%s.json' % uuid.uuid4(), 'x')
    file.write(j)
    path_to_file = os.path.realpath(file)
    response = FileResponse(open(path_to_file, 'rb'))
    file_name = file[5:]
    response['Content-Disposition'] = 'inline; filename=' + file_name
    return response
