# import the logging library
# Get an instance of a logger

from django import forms
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
    template_name = "generic_form.html"
    fields = ["type", "title", "description", "purpose", "status", "remarks"]

    def get_context_data(self, **kwargs):
        context = super(create_component_view, self).get_context_data(**kwargs)
        context['title'] = "Create New Component"
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
    logger = logging.getLogger("django")
    if request.method == "POST":
        logger.info("Processing POST from implemented_requirements_form_view...")
        results = request.POST
        component_id = results.get("component")
        comp = components.objects.get(pk=component_id)
        ctrl = controls.objects.get(pk=control_id)
        new_implemented_requirement = implemented_requirements.objects.create(control_id=ctrl)
        logger.info("Created new implemented_control. ID: " + str(new_implemented_requirement.id))

        for k, v in results.items():
            if "_" in k:
                logger.info("Processing field " + k + " with value " + v)
                item_lookup = k.split("_")
                if item_lookup[0] == "part":
                    f = parts.objects.get(pk=item_lookup[1])
                    logger.info(k + " is a prose item. Creating new statement")
                    new_statement = statements.objects.create()
                    logger.info("Created new statement with id " + str(new_statement.id))
                    new_statement.statement_id.add(f)
                    logger.info("Created part to statement relationship")
                    new_statement.save()
                    logger.info("Statement saved")
                    new_by_component = by_components.objects.create(component_uuid=comp, description=v)
                    new_by_component.save()
                    logger.info("by_component created and saved")
                    logger.info("Linked to component")
                    new_statement.by_components.add(new_by_component)
                    logger.info("by_component linked to statement")
                    new_statement.save()
                    logger.info("Statement saved")
                    new_implemented_requirement.statements.add(new_statement)
                    logger.info("Statement linked to implimented_requirement")
                    new_implemented_requirement.save()
                elif item_lookup[0] == "param":
                    f = params.objects.get(pk=item_lookup[1])
                    # Find Parameters in statement and add values to the by_component object, so they are stored at the most granular (statement) level
                    new_parameter = parameters.objects.create(param_id=f, values=v)
                    new_implemented_requirement.set_parameters.add(new_parameter)
                    new_implemented_requirement.save()
        context = {
            "success": "Object Saved", "post_data": request.POST,
            "new_implemented_requirement": new_implemented_requirement.to_html()
            }
        return render(request, "component_definition/implemented_requirements_form.html", context)
    else:
        ctrl = controls.objects.get(pk=control_id)
        component_list = []
        for component in components.objects.all():
            component_list.append((component.id, component.title))
        context = {
            "control": ctrl.to_html_form(), "control_id": control_id, "component_list": component_list
            }
        return render(request, "component_definition/implemented_requirements_form.html", context)
