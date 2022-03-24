import json

from ssp.models import *

"""
Some useful common functions
"""


def import_ssp(ssp_file="sample_data/ssp-example.json"):
    ssp_json = json.load(open(ssp_file))
    ssp_dict = ssp_json["system-security-plan"]
    new_ssp = system_security_plans()
    new_ssp.import_oscal(ssp_dict)
    new_ssp.save()
    return new_ssp
