import json
import logging

from ssp.models import system_security_plans


def import_ssp(ssp_file="sample_data/ssp-example.json"):
    logger = logging.getLogger("django")
    logger.info("Starting SSP import process")
    ssp_json = json.load(open(ssp_file))
    ssp_dict = ssp_json["system-security-plan"]
    if system_security_plans.objects.filter(uuid=ssp_dict["uuid"]).exists():
        system_security_plans.objects.get(uuid=ssp_dict["uuid"]).delete()
    new_ssp = system_security_plans()
    new_ssp.import_oscal(ssp_dict)
    new_ssp.save()
    return new_ssp
