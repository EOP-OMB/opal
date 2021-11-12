# Create your views here.
import logging
import os
import urllib

import django_filters
from django.contrib import messages
from django.core.files import File
from django.forms import modelformset_factory, Textarea
from django.shortcuts import *
from django.views import generic
from django.urls import reverse

from scripts.OSCAL_Catalog_import import run
from ssp.models.controls import *
from .forms import SystemSecurityPlan, ImportCatalogForm, SystemUserNewForm
from .models import system_control, system_security_plan, nist_control, control_parameter, control_statement, \
    system_user, user_role, person
from .models import test_evidence

def ssp_new(request):
    if request.method == "POST":
        form = SystemSecurityPlan(request.POST)
        if form.is_valid():
            ssp = form.save()
            return redirect('ssp:system_security_plan_detail_view', pk=ssp.pk)
    else:
        form = SystemSecurityPlan()
    return render(request, 'ssp/ssp_edit.html', {'form': form})


def ssp_edit(request, pk):
    ssp = get_object_or_404(system_security_plan, pk=pk)
    if request.method == "POST":
        form = SystemSecurityPlan(request.POST, instance=ssp)
        if form.is_valid():
            form.save()
            return redirect('ssp:system_security_plan_detail_view', pk=pk)
    else:
        form = SystemSecurityPlan(instance=ssp)
    return render(request, 'ssp/ssp_edit.html', {'form': form})


def system_control_edit(request, pk):
    sc = get_object_or_404(system_control, pk=pk)
    sc_FormSet = modelformset_factory(system_control, fields=('control_status', 'control_origination'))
    sc_paramFormSet = modelformset_factory(control_parameter, fields=('control_parameter_id', 'value'),
                                           widgets={'value': Textarea(attrs={'cols': 30, 'rows': 1})})
    sc_statementFormSet = modelformset_factory(control_statement,
                                               fields=('control_statement_id', 'control_statement_text'))
    if request.method == "POST":
        sc_paramFormSet = sc_paramFormSet(queryset=control_parameter.objects.filter(system_control=sc.id))
        if sc_paramFormSet.is_valid():
            sc_paramFormSet.save(commit=False)
            # parameter Titles are control title - parameter id
            sc_paramFormSet.title = sc.title + ' - ' + sc_paramFormSet.control_parameter_id
            # parameter short_name should be the control it relates to
            sc_paramFormSet.short_name = sc.short_name
            sc_paramFormSet.save()
        else:
            form_is_not_valid = True
        if sc_statementFormSet.is_valid():
            sc_statementFormSet.save(commit=False)
            # Statement Titles are control title - parameter id
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
    return render(request, 'ssp/system_control_edit.html',
                  {'object': sc, 'sc_formset': sc_formset, 'param_formset': param_formset,
                   'statement_formset': statement_formset})


class nist_control_list_view(generic.ListView):
    model = nist_control
    queryset = nist_control.objects.order_by('sort_id')


class nist_control_detail_view(generic.DetailView):
    model = nist_control


class evidence_list_view(generic.ListView):
    model = test_evidence


class evidence_detail_view(generic.DetailView):
    model = test_evidence

class system_control_list_view_filter(django_filters.FilterSet):
    class Meta:
        model = system_control
        fields = ['control_status', 'nist_control__group_title', 'control_primary_system']


class system_control_list_view(generic.ListView):
    model = system_control


class system_control_detail_view(generic.DetailView):
    model = system_control


class link_list_view(generic.ListView):
    model = link

class attachment_list_view(generic.ListView):
    model = attachment

class system_security_plan_list_view(generic.ListView):
    model = system_security_plan
    queryset = system_security_plan.objects.order_by('title')


class system_security_plan_detail_view(generic.DetailView):
    model = system_security_plan
    log = logging.getLogger(__name__)
    log.info('ssp ', object.__name__, 'viewed by')


def import_catalog(request):
    """For scanning file streams, ClamAV should be installed and clamd should be running in Powershell. Also pip install pyclamd for using Clam daemon in python
    (  https://www.clamav.net/documents/installing-clamav-on-windows & https://pypi.org/project/pyClamd/  )
    Note: There is another python module (clamd) which I tried first. It opens a UNIX socket which was not working with my Windows """

    try:
        import pyclamd
        cd = pyclamd.ClamdAgnostic()
        clamd_running = True
    except Exception as e:
        logging.debug(str(e))
        clamd_running = False

    if request.method == 'POST':
        form = ImportCatalogForm(request.POST, request.FILES)

        if form.is_valid():
            catalog = form.save(commit=False)

            """Uploaded JSON files will be saved without being scanned when ClamAV daemon is down"""

            if len(request.FILES) != 0:
                if clamd_running:
                    scan_results = cd.scan_stream(request.FILES['file'])
                    # scan_results = cd.scan_stream(cd.EICAR()) This is a test to see behavir when virus found
                    if scan_results is None:
                        catalog.file = request.FILES['file']
                else:
                    catalog.file = request.FILES['file']

            if form.cleaned_data['file_url']:
                result = urllib.request.urlretrieve(form.cleaned_data['file_url'])
                if clamd_running:
                    scan_results = cd.scan_stream(File(open(result[0], 'rb')))
                    if scan_results is None:
                        catalog.file.save(os.path.basename(form.cleaned_data['file_url']), File(open(result[0], 'rb')))
                else:
                    catalog.file.save(os.path.basename(form.cleaned_data['file_url']), File(open(result[0], 'rb')))

            if (clamd_running and scan_results is None) or not clamd_running:

                if request.user.is_authenticated:
                    catalog.user = request.user.username

                catalog_control_baseline, created = control_baseline.objects.get_or_create(title=catalog.title,
                                                                                           short_name=catalog.title)
                catalog.control_baseline = catalog_control_baseline

                if catalog.file_url:
                    catalog_link, created = link.objects.update_or_create(href=catalog.file_url, defaults={
                        'text': catalog.title,
                        'href': catalog.file_url
                    })
                    catalog_control_baseline.link = catalog_link
                    catalog_control_baseline.save()

                print("----file info----")
                print(catalog.file.name, catalog.file.path)
                print("-----------------")
                catalog.save()

                # form.save()
                if form.cleaned_data['file']:
                    file_path = str(catalog.file)
                    catalog_name = str(form.cleaned_data['file'])
                else:
                    file_path = form.cleaned_data['file_url']
                    file_path_list = file_path.split('/')
                    catalog_name = file_path_list[-1]

                # Uploaded files are in \uploads\catalog (\uploads is MEDIA_ROOT)
                added, updated = run(catalog.control_baseline, catalog.file.path, catalog_name)
                catalog.added_controls = added
                catalog.updated_controls = updated
                catalog.save()

                if clamd_running:
                    scan_news = "Virus scan accepted this file. "
                else:
                    scan_news = "Virus scan is down. "
                messages.success(request, scan_news + 'Imported NIST Catalog successfully. Added ' + str(
                    added) + ' and updated ' + str(updated) + ' NIST Controls.')
                return render(request, 'ssp/import_catalog.html', {'form': form})
                # return HttpResponse("data submitted successfully")
            elif scan_results is not None:
                messages.success(request, 'Virus scan rejected this file: ' + str(scan_results['stream']))
                return render(request, 'ssp/import_catalog.html', {'form': form})

        else:
            return render(request, 'ssp/import_catalog.html', {'form': form})
    else:
        form = ImportCatalogForm()
        return render(request, 'ssp/import_catalog.html', {'form': form})


def system_user_new(request, sspid, roleid):
    if request.method == "POST":
        form = SystemUserNewForm(request.POST)
        if form.is_valid():
            # person_id = form.cleaned_data['user']
            # person_obj = person.objects.get(id=person_id.id)
            person_obj = form.cleaned_data['user']
            ssp_obj = system_security_plan.objects.get(id=sspid)
            role_obj = user_role.objects.get(id=roleid)
            user_obj, created = system_user.objects.get_or_create(user=person_obj)
            if created:
                user_obj.title = role_obj.title
                user_obj.short_name = role_obj.short_name
                user_obj.save()
            user_obj.roles.add(role_obj)
            ssp_obj.system_users.add(user_obj)

            return redirect('ssp:system_security_plan_detail_view', pk=sspid)

    else:
        form = SystemUserNewForm()
    return render(request, 'ssp/system_user_new.html', {'form': form})


def oscal_json(request, objid, objurl):
    from django.contrib.contenttypes.models import ContentType
    url_list = objurl.split('_')
    del url_list[0]
    del url_list[-1]
    model_name = '_'.join(url_list)
    content_type = ContentType.objects.get(app_label=u'ssp', model=model_name)
    model_object = content_type.model_class()
    model_instance = model_object.objects.get(pk=objid)
    try:
        page_content = model_instance.get_serializer_json_OSCAL
    except:
        page_content = "No content. OSCAL JSON serializer might not exist for this  model."
    return render(request, 'ssp/oscal_json.html', {'result': page_content})


def clone_system_control(result, ssp, control):
    c = system_control.objects.get(pk=control)
    new_ssp = system_security_plan.objects.get(pk=ssp)
    clone = c.clone_control(new_ssp)
    return redirect('admin:ssp_system_control_change', clone.pk)

def add_system_control(ssp, nist_control_to_add, inherit_from_ssp="None"):
    s = system_security_plan.objects.get(pk=ssp)
    nc = nist_control.objects.get(pk=nist_control_to_add)
    new_control = system_control(title =s.title + ' ' + nc.label,
                                 short_name =nc.control_id + '-' + s.short_name,
                                 control_primary_system = s
                                 )
    new_control.save()
    if inherit_from_ssp != 'None':
        i = system_security_plan.objects.get(pk=inherit_from_ssp)
        if i.controls.filter(nist_control=nc).exists:
            source_control = i.controls.get(nist_control=nc)
            for p in source_control.control_parameters:
                new_control.control_parameters.add(p)
            for s in source_control.control_statements:
                new_control.control_statements.add(s)
    new_control.save()
    return new_control



