from django.shortcuts import render
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
            initial["by_components"] = self.kwargs["by_components"]
        return initial

    def get_context_data(self, **kwargs):
        context = super(create_implemented_requirements_view, self).get_context_data(**kwargs)
        context['form_title'] = "Create New Implemented Requirement"
        # And so on for more models
        return context


def implemented_requirements_form_view(request, control_id):
    if request.method == "POST":
        logger = logging.getLogger('debug')
        component_id = request.POST["component"]
        ctrl = catalog.models.controls.objects.get(pk=control_id)
        logger.debug("Just trying to see if logging is working")
        new_implemented_requirement = implemented_requirements.objects.create(control_id=ctrl)

        for statement in ctrl.parts.all():
            if statement.part_id in request.POST:
                new_statement = statements.objects.create()
                new_statement.statement_id.add(statement)
                new_statement.save()
                new_by_component = by_components.objects.create(
                    component_uuid=component_id, description=request.POST[statement.part_id]
                    )
                new_statement.by_components.add(new_by_component)
                new_statement.save()
                new_implemented_requirement.statements.add(new_statement)
                new_implemented_requirement.save()
                # Find Parameters in statement and add values to the by_component object, so they are stored at the most granular (statement) level
                if ctrl.params is not None:
                    for param in ctrl.params.all():
                        str_to_find = '{{ insert: param, ' + param.param_id + ' }}'
                        if statement.prose.find(str_to_find) >= 0:
                            new_parameter = parameters.objects.create(
                                param_id=param.param_id, values=request.POST[param.param_id]
                                )
                            new_by_component.set_parameters.add(new_parameter)
                            new_by_component.save()

        context = {
            "success": "Object Saved", "post_data": request.POST,
            "new_implemented_requirement": new_implemented_requirement.to_html()
            }
        return render(request, "component_definition/implemented_requirements_form.html", context)
    else:
        ctrl = catalog.models.controls.objects.get(pk=control_id)
        component_list = []
        for component in components.objects.all():
            component_list.append((component.id, component.title))
        context = {
            "control": ctrl.to_html_form(), "control_id": control_id, "component_list": component_list
            }
        return render(request, "component_definition/implemented_requirements_form.html", context)
