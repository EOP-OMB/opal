import pytest
from django.conf import settings
from django.test import Client
from django.urls import reverse
from model_bakery import baker

from catalog.models import catalogs, available_catalog_list
from catalog.views import import_catalog_task

pytestmark = pytest.mark.django_db

# Create your tests here.
# @pytest.fixture(scope='function', autouse=True)
# def get_sample_catalog_id(db):
#     host = settings.HOST_NAME
#     item = {}
#     new_catalog = import_catalog_task(item, host, test=True)
#     return new_catalog.id


def get_sample_catalog_id():
    sample_catalog = catalogs.objects.first()
    return sample_catalog.id


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
    url = reverse('catalog:catalog_detail_view', kwargs={'pk': get_sample_catalog_id()})
    response = c.get(url)
    assert response.status_code == 200


def test_control_detail_view(db):
    c = Client()
    cat = catalogs.objects.get(pk=get_sample_catalog_id())
    ctrl_list = cat.list_all_controls()
    ctrl = ctrl_list[0]
    url = reverse('catalog:control_detail_view', kwargs={'pk': ctrl.id})
    response = c.get(url)
    assert response.status_code == 200


def test_load_controls_view(db):
    c = Client()
    url = reverse('catalog:ajax_load_controls') + '?catalog=' + str(get_sample_catalog_id())
    response = c.get(url)
    assert response.status_code == 200


def test_load_statements_view(db):
    c = Client()
    cat = catalogs.objects.get(pk=get_sample_catalog_id())
    ctrl_list = cat.list_all_controls()
    ctrl = ctrl_list[0]
    url = reverse('catalog:ajax_load_controls') + '?control=' + str(ctrl.id)
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.slow
def test_import_catalog_view(db):
    c = Client()
    url = reverse('catalog:import_catalog_view', kwargs={'catalog_id': available_catalog_list.objects.first().id})
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
