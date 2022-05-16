from django.test import TestCase
from ssp.models import *
import json


# Create your tests here.

class ssp_import_test(TestCase):

    def setUp(self):
        self.ssp_file = "sample_data/ssp-example.json"
        self.ssp_json = json.load(open(self.ssp_file))
        self.ssp_dict = self.ssp_json["system-security-plan"]
        self.new_ssp = system_security_plans()
        self.new_ssp.import_oscal(self.ssp_dict)
        self.new_ssp.save()

    def test_import(self):
        obj = system_security_plans.objects.get(uuid=self.new_ssp.uuid)
        self.assertEqual(obj.metadata.version, "1.0")
        self.assertEqual(obj.metadata.oscal_version, "1.0.0")
        self.assertEqual(obj.metadata.title, "Enterprise Logging and Auditing System Security Plan")
