from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from catalog.models import *
from ssp.models import *
from django.apps import apps
from opal.settings import USER_APPS
from .functions import search_for_uuid


# Create your views here.

class IndexView(TemplateView):
    template_name = "index.html"
    context_object_name = "obj"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['catalog_list'] = catalogs.objects.all()
        context['ssp_list'] = system_security_plans.objects.all()
        # And so on for more models
        return context


class DatabaseStatusView(TemplateView):
    template_name = "db_status.html"
    context_object_name = "obj"

    def get_context_data(self, **kwargs):
        context = super(DatabaseStatusView, self).get_context_data(**kwargs)
        model_list = []
        for a in USER_APPS:
            app_models = apps.get_app_config(a).get_models()
            for m in app_models:
                if m.objects.count() > 0:
                    s = m.__name__ + ":" + str(m.objects.count())
                    model_list.append(s)
        model_list.sort()
        context["model_list"] = model_list
        return context


def permalink(request, uuid):
    redirect_url = "error_404_view"
    obj = search_for_uuid(uuid)
    try:
        redirect_url = obj.get_absolute_url()
    except AttributeError as e:
        err_msg = e
    return redirect(to=redirect_url)


def error_404_view(request, exception):
    template_name = "404.html"
    context_object_name = "obj"

