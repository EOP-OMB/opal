from django.test import TestCase
import json

from catalog.models import catalogs
from .models import *
from .functions import search_for_uuid

# Create your tests here.
class modelTests(TestCase):
    def setUp(self):
        self.catalog_file = "sample_data/basic-catalog.json"
        self.catalog_json = json.load(open(self.catalog_file))
        self.catalog_dict = self.catalog_json["catalog"]
        self.new_catalog = catalogs()
        self.new_catalog.import_oscal(self.catalog_dict)
        self.new_catalog.save()

    def test_permalink(self):
        pass


    def test_db_status(self):
        pass


    def test_authentication_view(self):
        pass



    def test_saml_authentication(self):
        pass


    def test_attrs(self):
        pass


    def test_metadata(self):
        pass
