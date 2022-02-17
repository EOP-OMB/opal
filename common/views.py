from django.shortcuts import render
from django.views.generic import TemplateView
from catalog.models import *
from ssp.models import *


# Create your views here.

class base_view(TemplateView):
    template_name = "base.html"
    context_object_name = "obj"

    def get_context_data(self, **kwargs):
        context = super(base_view, self).get_context_data(**kwargs)
        context['catalog_list'] = catalogs.objects.all()
        context['ssp_list'] = system_security_plans.objects.all()
        # And so on for more models
        return context