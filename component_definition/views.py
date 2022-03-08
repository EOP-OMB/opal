from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import *


# Create your views here.

class component_list_view(ListView):
    model = components
    context_object_name = "context_list"
    template_name = "generic_list.html"


class component_detail_view(DetailView):
    model = components
    context_object_name = "context"
    template_name = "generic_detail.html"


class create_component_view(CreateView):
    model = components
    template_name = "component_definition/component_form.html"
    fields = ["type", "title", "description", "purpose", "status", "remarks"]
