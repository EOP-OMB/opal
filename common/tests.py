from django.test import TestCase
import json
from django.test import Client
from django.urls import reverse
from catalog.models import catalogs
from .models import *
from .functions import search_for_uuid

# Create your tests here.

def test_index_view(db):
    c = Client()
    url = reverse('home_page')
    response = c.get(url)
    assert response.status_code == 200



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
