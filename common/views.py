from django.shortcuts import render
from django.views.generic import TemplateView
from catalog.models import *
from ssp.models import *
from django.apps import apps


# Create your views here.

class IndexView(TemplateView):
    template_name = "base.html"
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
        context = super(DatabaseStatusView,self).get_context_data(**kwargs)
        model_list = []
        for m in apps.get_models():
            if m.objects.count() > 0:
                s = m.__name__ + ":" + str(m.objects.count())
                model_list.append(s)
        model_list.sort()
        context["model_list"] = model_list
        return context
