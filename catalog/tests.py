import pytest
import json

from common.models import metadata
from catalog.models import catalogs
from ctrl_profile.models import profiles, imports
from component.models import components
from django.test import Client, TestCase
from django.urls import reverse
from model_bakery import baker
from model_bakery.recipe import Recipe, foreign_key
from common.views import load_catalog_import_list


# Create your tests here.
class catalog_model_tests(TestCase):
    def testCatalogModel(self):
        self.catalog = baker.make(catalogs, _fill_optional=True)
        assert self.catalog == catalogs.objects.get(id=self.catalog.id)


@pytest.fixture(scope='module')
def init_database(django_db_blocker):
    load_catalog_import_list()


@pytest.fixture(scope='module')
def load_sample_catalog(django_db_blocker):
    catalog_file = "sample_data/basic-catalog.json"
    catalog_json = json.load(open(catalog_file))
    catalog_dict = catalog_json["catalog"]
    with django_db_blocker.unblock():
        new_catalog = catalogs()
        new_catalog.import_oscal(catalog_dict)
        new_catalog.save()
        # create a new profiles for the imported catalog
        new_metadata = metadata.objects.create(title=new_catalog.metadata.title)
        new_profile = profiles.objects.create(
            metadata=new_metadata
            )
        new_profile.save()
        url = "https://test_host/" + new_catalog.get_permalink()
        new_profile.imports.add(imports.objects.create(href=url, import_type="catalog"))
        new_profile.save()
        # create components for any groups in the catalog
        for group in new_catalog.groups.all():
            new_component = components.objects.get_or_create(
                type="policy", title=group.title + " Policy",
                description="This Component Policy was automatically created durring the import of " + new_metadata.title,
                purpose="This Component Policy was automatically created durring the import of " + new_metadata.title,
                status="under-development"
                )
    return new_catalog.id


def test_catalog_index_view(db, load_sample_catalog):
    c = Client()
    url = reverse('catalog:catalog_index_view')
    response = c.get(url)
    assert response.status_code == 200


def test_catalog_list_view(db, load_sample_catalog):
    c = Client()
    url = reverse('catalog:catalog_list_view')
    response = c.get(url)
    assert response.status_code == 200


def test_catalog_detail_view(db, load_sample_catalog):
    c = Client()
    url = reverse('catalog:catalog_detail_view', kwargs={'pk': load_sample_catalog})
    response = c.get(url)
    assert response.status_code == 200


def test_control_detail_view(db, load_sample_catalog):
    c = Client()
    cat = catalogs.objects.get(pk=load_sample_catalog)
    ctrl_list = cat.list_all_controls()
    ctrl = ctrl_list[0]
    url = reverse('catalog:control_detail_view', kwargs={'pk': ctrl.id})
    response = c.get(url)
    assert response.status_code == 200


def test_load_controls_view(db, load_sample_catalog):
    c = Client()
    url = reverse('catalog:ajax_load_controls') + '?catalog=' + str(load_sample_catalog)
    response = c.get(url)
    assert response.status_code == 200


def test_load_statements_view(db, load_sample_catalog):
    c = Client()
    cat = catalogs.objects.get(pk=load_sample_catalog)
    ctrl_list = cat.list_all_controls()
    ctrl = ctrl_list[0]
    url = reverse('catalog:ajax_load_controls') + '?control=' + str(ctrl.id)
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.slow
def test_import_catalog_view(db):
    c = Client()
    response_app_init = c.get(reverse('common:app_init'))
    url = reverse('catalog:import_catalog_view', kwargs={'catalog_id': catalogs.objects.first().id})
    response = c.get(url)
    assert response.status_code == 302
    # assert catalogs.objects.filter(metadata__title='NIST Special Publication 800-53 Revision 5 MODERATE IMPACT BASELINE').exists()
    # assert profiles.objects.filter(metadata__title='NIST Special Publication 800-53 Revision 5 MODERATE IMPACT BASELINE').exists()


def test_load_controls(db, load_sample_catalog):
    c = Client()
    cat = catalogs.objects.first()
    url = reverse('catalog:ajax_load_controls') + '?catalog=' + str(cat.id)
    response = c.get(url)
    assert response.status_code == 200


def test_load_statements(db, load_sample_catalog):
    c = Client()
    cat = catalogs.objects.first()
    ctrl_list = cat.list_all_controls()
    ctrl = ctrl_list[0]
    url = reverse('catalog:ajax_load_statements') + '?control=' + str(ctrl.id)
    response = c.get(url)
    assert response.status_code == 200


def test_load_params(db, load_sample_catalog):
    c = Client()
    cat = catalogs.objects.first()
    ctrl_list = cat.list_all_controls()
    ctrl = ctrl_list[0]
    url = reverse('catalog:ajax_load_params') + '?control=' + str(ctrl.id)
    response = c.get(url)
    assert response.status_code == 200
