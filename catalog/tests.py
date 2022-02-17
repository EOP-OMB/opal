from django.test import TestCase
import json
from catalog.models import *

# Create your tests here.

class catalog_import_test(TestCase):
    def test_import(self):
        catalog_file = "sample_data/basic-catalog.json"
        catalog_json = json.load(open(catalog_file))
        catalog_dict = catalog_json["catalog"]
        new_catalog = catalogs()
        new_catalog.import_oscal(catalog_dict)
        new_catalog.save()

        obj = catalogs.objects.get(uuid="74c8ba1e-5cd4-4ad1-bbfd-d888e2f6c724")
        # self.assertEqual(obj.metadata.published, "2020-02-02T11:01:04.736-04:00")
        # self.assertEqual(obj.metadata.last_modified, "2021-06-08T13:57:28.355446-04:00")
        self.assertEqual(obj.metadata.version, "1.0")
        self.assertEqual(obj.metadata.oscal_version, "1.0.0")
        self.assertEqual(
            obj.metadata.remarks,
            "The following is a short excerpt from [ISO/IEC 27002:2013](https://www.iso.org/standard/54533.html), *Information technology — Security techniques — Code of practice for information security controls*. This work is provided here under copyright \"fair use\" for non-profit, educational purposes only. Copyrights for this work are held by the publisher, the International Organization for Standardization (ISO)."
            )



