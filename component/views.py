from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import component_statement_form, select_control_statements_form
from catalog.views import get_statements
from .models import *
from ctrl_profile.models import profiles


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


def create_component_statement(request):
    """
    Create a statement associated with a component that addresses one or more Control requirements
    """
    if request.method == 'POST':
        comp_id = components.objects.get(pk=request.POST['component_uuid'])
        impl_description = request.POST['description']
        impl_status = request.POST['implementation_status']
        ctrl_id = controls.objects.get(pk=request.POST['controls'])

        new_by_comp, created = by_components.objects.get_or_create(component_uuid=comp_id, description=impl_description, implementation_status=impl_status)
        new_by_comp.save()
        logger = logging.getLogger('django')
        logger.info("Created new by_component model? %s.  by_component_id = %s" % (created, new_by_comp.id))
        for stmt in request.POST['statements']:
            new_stmt = statements()
            new_stmt.save()
            logger.info("New statement, statement_id = %s" % new_stmt.id)
            new_stmt.statement_id.add(stmt)
            new_stmt.by_components.add(new_by_comp.id)
            logger.info("Added new statement to new by_component")
            new_implemented_requirement, created = implemented_requirements.objects.get_or_create(control_id=ctrl_id)
            new_implemented_requirement.save()
            logger.info("New implemented_requirement? %s -- implemented_requirement_id = %s" % (created, new_implemented_requirement.id))
            new_implemented_requirement.statements.add(new_stmt.id)
            new_implemented_requirement.by_components.add(new_by_comp.id)
            if comp_id.control_implementations.count() == 0:
                logger.info("Looks like this is the first control implemented by this component.  Adding control_implementation object")
                comp_control_implementation = control_implementations()
                comp_control_implementation.save()
                comp_id.control_implementations.add(comp_control_implementation.id)
                logger.info("Added new control_implementation for component")
            comp_id.control_implementations.first().implemented_requirements.add(new_implemented_requirement.id)
            comp_id.save()
            logger.info("Added new control_implementation to component %s." % comp_id.title)
        logger.info("Looking for parameters")
        param_list = ctrl_id.params.all()
        for p in param_list:
            param_value = request.POST[p.param_id]
            if param_value != '':
                new_param_id, created = parameters.objects.get_or_create(param_id=p,values=param_value)
                comp_id.control_implementations.first().set_parameters.add(new_param_id)
        return HttpResponseRedirect(comp_id.get_absolute_url())
    else:
        profile_id = request.GET.get('profile_id', default=None)
        ctrl_id = request.GET.get('ctrl_id', default=None)
        initial_dict = {}
        statement_list = []
        if profile_id:
            initial_dict['profiles'] = profile_id
            selected_profile = profiles.objects.get(pk=profile_id)
            initial_dict['controls'] = selected_profile.list_all_controls()
        if ctrl_id:
            initial_dict['controls'] = ctrl_id
            ctrl_statements = get_statements(ctrl_id)
            for item in ctrl_statements:
                statement_list.append((item["value"], item["display"]))
        if initial_dict != {}:
            ctrl_selection_form = select_control_statements_form(initial=initial_dict)
            if statement_list:
                ctrl_selection_form.fields['statements'].choices = statement_list
        else:
            ctrl_selection_form = select_control_statements_form()

        comp_id = request.GET.get('comp_id', default=None)
        if comp_id:
            comp_statement_form = component_statement_form(initial={'component_uuid': comp_id})
        else:
            comp_statement_form = component_statement_form()

    context = {
        "comp_form": comp_statement_form,
        "ctrl_form": ctrl_selection_form
        }
    return render(request, "component/requirements_by_component.html", context)
