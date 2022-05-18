import pytest
from .factory import *
import json

from common.models import metadata
from catalog.models import catalogs
from profile.models import profile, imports
from component.models import components
from django.test import Client
from django.urls import reverse


# Create your tests here.

@pytest.fixture(scope='module')
def load_sample_catalog(django_db_blocker):
    catalog_file = "sample_data/basic-catalog.json"
    catalog_json = json.load(open(catalog_file))
    catalog_dict = catalog_json["catalog"]
    with django_db_blocker.unblock():
        new_catalog = catalogs()
        new_catalog.import_oscal(catalog_dict)
        new_catalog.save()
        # create a new profile for the imported catalog
        new_metadata = metadata.objects.create(title=new_catalog.metadata.title)
        new_profile = profile.objects.create(
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


@pytest.mark.django_db
def test_catalog_index_view(db, load_sample_catalog):
    c = Client()
    url = reverse('catalog:catalog_index_view')
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_catalog_list_view(load_sample_catalog):
    c = Client()
    url = reverse('catalog:catalog_list_view')
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_catalog_detail_view(load_sample_catalog):
    c = Client()
    url = reverse('catalog:catalog_detail_view', kwargs={'pk': load_sample_catalog})
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_control_detail_view(load_sample_catalog):
    c = Client()
    cat = catalogs.objects.get(pk=load_sample_catalog)
    ctrl_list = cat.list_all_controls()
    ctrl = ctrl_list[0]
    url = reverse('catalog:control_detail_view', kwargs={'pk': ctrl.id})
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_import_catalog_view():
    c = Client()
    url = reverse('catalog:import_catalog_view', kwargs={'catalog_link': 'nist_sp_800_53_rev_5_moderate_baseline'})
    response = c.get(url)
    assert response.status_code == 302


#     assert response.body.find()

@pytest.mark.django_db
def test_load_controls(load_sample_catalog):
    c = Client()
    prfl = profile.objects.first()
    url = reverse('catalog:ajax_load_controls') + '?profile=' + str(prfl.id)
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_load_statements(load_sample_catalog):
    c = Client()
    cat = catalogs.objects.get(pk=load_sample_catalog)
    ctrl_list = cat.list_all_controls()
    ctrl = ctrl_list[0]
    url = reverse('catalog:ajax_load_statements') + '?control=' + str(ctrl.id)
    response = c.get(url)
    assert response.status_code == 200

