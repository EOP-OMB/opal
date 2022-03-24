from django.test import TestCase
from ssp.models import *
import json


# Create your tests here.

class ssp_import_test(TestCase):
    def test_import(self):
        ssp_file = "sample_data/ssp-example.json"
        ssp_json = json.load(open(ssp_file))
        ssp_dict = ssp_json["system-security-plan"]
        new_ssp = system_security_plans()
        new_ssp.import_oscal(ssp_dict)
        new_ssp.save()

        obj = system_security_plans.objects.get(uuid="cff8385f-108e-40a5-8f7a-82f3dc0eaba8")
        self.assertEqual(obj.metadata.version, "1.0")
        self.assertEqual(obj.metadata.oscal_version, "1.0.0")
        self.assertEqual(obj.metadata.title, "Enterprise Logging and Auditing System Security Plan")
