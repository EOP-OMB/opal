import json
import logging
import os.path

from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from formtools.wizard.views import CookieWizardView

from common.forms import back_matter_form
from ssp.models import system_security_plans
# from ssp.forms import system_characteristics_form


def import_ssp_view(request, ssp_file):
    logger = logging.getLogger("django")
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
    return redirect('home_page')


def import_ssp(ssp_file):
    logger = logging.getLogger("django")
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


class ssp_list_view(ListView):
    model = system_security_plans
    context_object_name = "context_list"
    add_new_url = reverse_lazy('admin:ssp_system_security_plans_add')
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


# class ssp_wizard(CookieWizardView):
#     form_list = [system_characteristics_form, back_matter_form]
#
#     def done(self, form_list, **kwargs):
#         return render(self.request, reverse(ssp_detail_view),{
#             'form_data': [form.cleaned_data for form in form_list],
#         })
