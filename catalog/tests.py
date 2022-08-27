import pytest
from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse
from model_bakery import baker

from catalog.models import catalogs
from catalog.views import import_catalog_task
from common.management.commands.bootstrap import load_catalog_import_list


# Create your tests here.
@pytest.fixture(scope='module')
def init_database(django_db_blocker):
    load_catalog_import_list()


@pytest.fixture(scope='module', autouse=True)
def load_sample_catalog(django_db_blocker):
    host = settings.HOST_NAME
    item = {}
    new_catalog = import_catalog_task(item, host, test=True)
    return new_catalog.id


def test_catalog_index_view(db):
    c = Client()
    url = reverse('catalog:catalog_index_view')
    response = c.get(url)
    assert response.status_code == 200


def test_catalog_list_view(db):
    c = Client()
    url = reverse('catalog:catalog_list_view')
    response = c.get(url)
    assert response.status_code == 200


def test_catalog_detail_view(db):
    c = Client()
    url = reverse('catalog:catalog_detail_view', kwargs={'pk': load_sample_catalog})
    response = c.get(url)
    assert response.status_code == 200


def test_control_detail_view(db):
    c = Client()
    cat = catalogs.objects.get(pk=load_sample_catalog)
    ctrl_list = cat.list_all_controls()
    ctrl = ctrl_list[0]
    url = reverse('catalog:control_detail_view', kwargs={'pk': ctrl.id})
    response = c.get(url)
    assert response.status_code == 200


def test_load_controls_view(db):
    c = Client()
    url = reverse('catalog:ajax_load_controls') + '?catalog=' + str(load_sample_catalog)
    response = c.get(url)
    assert response.status_code == 200


def test_load_statements_view(db):
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
    url = reverse('catalog:import_catalog_view', kwargs={'catalog_id': catalogs.objects.first().id})
    response = c.get(url)
    assert response.status_code == 302
    # assert catalogs.objects.filter(metadata__title='NIST Special Publication 800-53 Revision 5 MODERATE IMPACT BASELINE').exists()
    # assert profiles.objects.filter(metadata__title='NIST Special Publication 800-53 Revision 5 MODERATE IMPACT BASELINE').exists()


def test_load_controls(db):
    c = Client()
    cat = catalogs.objects.first()
    url = reverse('catalog:ajax_load_controls') + '?catalog=' + str(cat.id)
    response = c.get(url)
    assert response.status_code == 200


def test_load_statements(db):
    c = Client()
    cat = catalogs.objects.first()
    ctrl_list = cat.list_all_controls()
    ctrl = ctrl_list[0]
    url = reverse('catalog:ajax_load_statements') + '?control=' + str(ctrl.id)
    response = c.get(url)
    assert response.status_code == 200


def test_load_params(db):
    c = Client()
    cat = catalogs.objects.first()
    ctrl_list = cat.list_all_controls()
    ctrl = ctrl_list[0]
    url = reverse('catalog:ajax_load_params') + '?control=' + str(ctrl.id)
    response = c.get(url)
    assert response.status_code == 200
