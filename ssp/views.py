from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from ssp.models import *

# Create your views here.

class ssp_list_view(ListView):
    model = system_security_plans
    context_object_name = "ssp_list"
    template_name = "ssp/ssp_list.html"

class ssp_detail_view(DetailView):
    model = system_security_plans
    context_object_name = "ssp"
    template_name = "ssp/ssp_detail.html"

class ssp_list_view(ListView):
    model = system_security_plans
    context_object_name = "ssp_list"
    template_name = "ssp/ssp_list.html"

class ssp_detail_view(DetailView):
    model = system_security_plans
    context_object_name = "ssp"
    template_name = "ssp/ssp_detail.html"