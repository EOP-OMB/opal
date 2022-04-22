from django.test import TestCase
import json
from catalog.models import catalogs


# Create your tests here.

class catalog_import_test(TestCase):

    def setUp(self):
        self.catalog_file = "sample_data/basic-catalog.json"
        self.catalog_json = json.load(open(self.catalog_file))
        self.catalog_dict = self.catalog_json["catalog"]
        self.new_catalog = catalogs()
        self.new_catalog.import_oscal(self.catalog_dict)
        self.new_catalog.save()

    def test_import(self):
        self.assertEqual(self.new_catalog.metadata.version, "1.0")
        self.assertEqual(self.new_catalog.metadata.oscal_version, "1.0.0")
        self.assertEqual(
            self.new_catalog.metadata.remarks,
            "The following is a short excerpt from [ISO/IEC 27002:2013](https://www.iso.org/standard/54533.html), *Information technology — Security techniques — Code of practice for information security controls*. This work is provided here under copyright \"fair use\" for non-profit, educational purposes only. Copyrights for this work are held by the publisher, the International Organization for Standardization (ISO)."
            )


