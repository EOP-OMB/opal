# Create your views here.
from django.shortcuts import *
from django.views import generic
from django.forms import modelformset_factory, modelform_factory, Textarea

from .models import system_control, system_security_plan, nist_control, control_parameter, control_statement
from .forms import SystemSecurityPlan


def ssp_new(request):
    if request.method == "POST":
        form = SystemSecurityPlan(request.POST)
        if form.is_valid():
            ssp = form.save()
            return redirect('system_security_plan_detail_view', pk=ssp.pk)
    else:
        form = SystemSecurityPlan()
    return render(request, 'ssp/ssp_edit.html', {'form': form})


def ssp_edit(request, pk):
    ssp = get_object_or_404(system_security_plan, pk=pk)
    if request.method == "POST":
        form = SystemSecurityPlan(request.POST, instance=ssp)
        if form.is_valid():
            form.save()
            return redirect('system_security_plan_detail_view', pk=pk)
    else:
        form = SystemSecurityPlan(instance=ssp)
    return render(request, 'ssp/ssp_edit.html', {'form': form})


def system_control_edit(request, pk):
    sc = get_object_or_404(system_control, pk=pk)
    sc_FormSet = modelformset_factory(system_control,fields=('control_status','control_origination'))
    sc_paramFormSet = modelformset_factory(control_parameter, fields=('control_parameter_id','value'), widgets={'value': Textarea(attrs={'cols':30,'rows':1})})
    sc_statementFormSet = modelformset_factory(control_statement, fields=('control_statement_id','control_statement_text'))
    if request.method == "POST":
        sc_paramFormSet = sc_paramFormSet(queryset=control_parameter.objects.filter(system_control=sc.id))
        if sc_paramFormSet.is_valid():
            sc_paramFormSet.save(commit=False)
            # paramater Titles are control title - paramater id
            sc_paramFormSet.title = sc.title + ' - ' + sc_paramFormSet.control_parameter_id
            # paramater short_name should be the control it relates to
            sc_paramFormSet.short_name = sc.short_name
            sc_paramFormSet.save()
        else:
            form_is_not_valid = True
        if sc_statementFormSet.is_valid():
            sc_statementFormSet.save(commit=False)
            # Statement Titles are control title - paramater id
            sc_statementFormSet.title = sc.title + ' - ' + sc_statementFormSet.control_statement_id
            # Statement short_name should be the control it relates to
            sc_statementFormSet.short_name = sc.short_name
            sc_statementFormSet.save()
        else:
            form_is_not_valid = True
        if sc_FormSet.is_valid():
            sc_FormSet.save()
        else:
            form_is_not_valid = True
        if not form_is_not_valid:
            return redirect('ssp/system_control_edit.html', pk=pk)
    else:
        sc_formset = sc_FormSet(queryset=system_control.objects.filter(pk=sc.id))
        param_formset = sc_paramFormSet(queryset=control_parameter.objects.filter(system_control=sc.id))
        statement_formset = sc_statementFormSet(queryset=control_statement.objects.filter(system_control=sc.id))
    return render(request, 'ssp/system_control_edit.html', {'object': sc,'sc_formset': sc_formset,'param_formset':param_formset,'statement_formset':statement_formset})

class nist_control_list_view(generic.ListView):
    model = nist_control
    queryset = nist_control.objects.order_by('sort_id')



class nist_control_detail_view(generic.DetailView):
    model = nist_control


class system_control_list_view(generic.ListView):
    model = system_control


class system_control_detail_view(generic.DetailView):
    model = system_control


class system_security_plan_list_view(generic.ListView):
    model = system_security_plan


class system_security_plan_detail_view(generic.DetailView):
    model = system_security_plan
