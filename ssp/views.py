import json
import logging
import os.path

from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from ssp.models import system_security_plans, metadata, system_characteristics, system_implementations
from ssp.forms import system_security_plansForm


def import_ssp_view(ssp_file):
    logger = logging.getLogger("__name__")
    if ssp_file == 'ssp-example.json':
        ssp_file = 'sample_data/ssp-example.json'
    else:
        if not os.path.exists(ssp_file):
            logger.error(ssp_file + " does not exist.")
            context = {
                'msg': ssp_file + " does not exist."
            }
            return redirect('common.views.error_404_view')
    logger.info("Starting SSP import process")
    new_ssp = import_ssp(ssp_file)
    context = {
        'msg': new_ssp.metadata.title + " imported from " + ssp_file
    }
    # TODO this should redirect to the SSP list and should include the context message
    return redirect('home_page')


def import_ssp(ssp_file):
    logger = logging.getLogger("__name__")
    ssp_json = json.load(open(ssp_file))
    ssp_dict = ssp_json["system-security-plan"]
    if system_security_plans.objects.filter(uuid=ssp_dict["uuid"]).exists():
        logger.info("SSP with uuid " + ssp_dict["uuid"] + " already exists. Deleteing...")
        system_security_plans.objects.get(uuid=ssp_dict["uuid"]).delete()
        logger.info("SSP with uuid " + ssp_dict["uuid"] + " deleted.")
    new_ssp = system_security_plans()
    new_ssp.import_oscal(ssp_dict)
    new_ssp.save()
    return new_ssp


def ssp_form_view(request):
    context = {}
    form = system_security_plansForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        new_metadata = metadata.objects.create(
            title=form.data['title'],
            published=form.data['published'],
            last_modified=form.data['last_modified'],
            version=form.data['version'],
            oscal_version=form.data['oscal_version']
        )
        for location in form.data['locations']:
            new_metadata.locations.add(location)
        for party in form.data['responsible_parties']:
            new_metadata.responsible_parties.add(party)
        new_metadata.save()

        new_system_characteristics = system_characteristics.objects.create(
            system_name=form.data['system_name'],
            system_name_short=form.data['system_name_short'],
            description=form.data['description'],
            security_sensitivity_level=form.data['security_sensitivity_level'],
            security_impact_level=form.data['security_impact_level'],
            security_objective_confidentiality=form.data['security_objective_confidentiality'],
            security_objective_integrity=form.data['security_objective_integrity'],
            security_objective_availability=form.data['security_objective_availability'],
            status=form.data['status'],
            authorization_boundary=form.data['authorization_boundary'],
            network_architecture=form.data['network_architecture'],
            data_flow=form.data['data_flow']
        )

        new_system_implementation = system_implementations.objects.create()
        for authorization in form.data['leveraged_authorizations']:
            new_system_implementation.leveraged_authorizations.add(authorization)
        for component in form.data['components']:
            new_system_implementation.components.add(component)
        for item in form.data['inventory_items']:
            new_system_implementation.inventory_items.add(item)
        new_system_implementation.save()

        new_ssp = system_security_plans.objects.create(metadata=new_metadata, system_characteristics=new_system_characteristics, system_implementation=new_system_implementation, import_profile=form.data['import_profile'])
        redirect(reverse('ssp:ssp_detail_view', kwargs={'id': new_ssp.id}))

    context['form'] = form
    return render(request, "generic_form.html", context)


class ssp_list_view(ListView):
    model = system_security_plans
    context_object_name = "context_list"
    add_new_url = reverse_lazy('ssp:add_new_ssp_view')
    extra_context = {
        'title': 'System Security Plans',
        'add_url': add_new_url,
        'model_name': model._meta.verbose_name
    }
    template_name = "generic_list.html"


class ssp_detail_view(DetailView):
    model = system_security_plans
    context_object_name = "context"
    template_name = "generic_detail.html"
