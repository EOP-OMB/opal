import logging

from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django import forms

import catalog.models
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
    template_name = "generic_form.html"
    fields = ["type", "title", "description", "purpose", "status", "remarks"]

    def get_context_data(self, **kwargs):
        context = super(create_component_view, self).get_context_data(**kwargs)
        context['form_title'] = "Create New Component"
        # And so on for more models
        return context


class create_parameter_view(CreateView):
    model = parameters
    template_name = "generic_form.html"
    fields = ["values", "param_id"]

    def get_initial(self):
        initial = {}
        if 'param_id' in self.kwargs.keys():
            initial["param_id"] = self.kwargs["param_id"]
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['param_id'].widget = forms.HiddenInput()
        return form

    def get_context_data(self, **kwargs):
        context = super(create_parameter_view, self).get_context_data(**kwargs)
        context['form_title'] = "Create New Parameter Value"
        # And so on for more models
        return context


class create_implemented_requirements_view(CreateView):
    model = implemented_requirements
    template_name = "generic_form.html"
    field_list = []
    for field in model._meta.get_fields(include_hidden=False):
        if field.editable:
            field_list.append(field.name)
    fields = field_list

    def get_initial(self):
        initial = {}
        if 'control_id' in self.kwargs.keys():
            initial["control_id"] = self.kwargs["control_id"]
        if 'by_components' in self.kwargs.keys():
            initial["by_components"] = self.kwargs("by_components")
        return initial

    def get_context_data(self, **kwargs):
        context = super(create_implemented_requirements_view, self).get_context_data(**kwargs)
        context['form_title'] = "Create New Implemented Requirement"
        # And so on for more models
        return context


def implemented_requirements_form_view(request, control_id):
    if request.method == "POST":
        component_id = request.POST["component"]
        ctrl = catalog.models.controls.objects.get(pk=control_id)
        for statement in ctrl.parts:

        new_by_component = by_components.objects.create(component_uuid=component_id)
        new_implimented_requirement = implemented_requirements.objects.create(
            control_id=control_id,

            )

        request.POST
        context = {"success": "Object Saved",
            "post_data": request.POST}
        return render(request, "component_definition/implemented_requirements_form.html",context)
    else:
        ctrl = catalog.models.controls.objects.get(pk=control_id)
        component_list = []
        for component in components.objects.all():
            component_list.append((component.id, component.title))
        context = {"control": ctrl.to_html_form(),
            "control_id" : control_id,
            "component_list" : component_list}
        return render(request, "component_definition/implemented_requirements_form.html", context)
