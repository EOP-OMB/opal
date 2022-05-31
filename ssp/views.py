import os.path
import urllib.parse

from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
import json
from ssp.models import *


# Create your views here.

class ssp_list_view(ListView):
    model = system_security_plans
    context_object_name = "context_list"
    template_name = "generic_list.html"


class ssp_detail_view(DetailView):
    model = system_security_plans
    context_object_name = "context"
    template_name = "generic_detail.html"


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
    ssp_json = json.load(open(ssp_file))
    ssp_dict = ssp_json["system-security-plan"]
    if system_security_plans.objects.filter(uuid=ssp_dict["uuid"]).exists():
        logger.info("SSP with uuid " + ssp_dict["uuid"] + " already exists. Deleteing...")
        system_security_plans.objects.get(uuid=ssp_dict["uuid"]).delete()
        logger.info("SSP with uuid " + ssp_dict["uuid"] + " deleted.")
    new_ssp = system_security_plans()
    new_ssp.import_oscal(ssp_dict)
    new_ssp.save()
    context = {
        'msg': new_ssp.metadata.title + " imported from " + ssp_file
        }
    return redirect('home_page')