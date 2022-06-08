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
        profile_id = request.POST['profiles']
        new_by_comp = by_components(component_uuid_id=request.POST['component_uuid'], description=request.POST['description'], implementation_status=request.POST['implementation_status'], control_uuid_id=request.POST['control'])
        new_by_comp.save()
        if type(request.POST['statements']) is list:
            for stmt in request.POST['statements']:
                new_stmt = statements()
                new_stmt.save()
                new_stmt.statement_id.add(stmt)
                new_stmt.by_components.add(new_by_comp.id)
        else:
            new_stmt = statements()
            new_stmt.save()
            new_stmt.statement_id.add(request.POST['statements'])
            new_stmt.by_components.add(new_by_comp.id)

        return HttpResponseRedirect(reverse('control_profile:profile_detail_view', kwargs={'pk': profile_id}))
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
            statmts = get_statements(ctrl_id)
            for item in statmts:
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
