import uuid
from django.urls import reverse
from catalog.models import catalogs, available_catalog_list, tests, controls

import pytest

from model_bakery import baker
# Add generators for custom field types
from model_bakery.random_gen import gen_m2m, gen_string, gen_text
baker.generators.add('common.models.ShortTextField', gen_string)
baker.generators.add('ckeditor.fields.RichTextField', gen_text)
baker.generators.add('common.models.properties_field', gen_m2m)

pytestmark = pytest.mark.django_db


def test_catalog_index_view(admin_client):
    baker.make('catalog.catalogs',_quantity=10)
    url = reverse('catalog:catalog_index_view')
    response = admin_client.get(url)
    assert response.status_code == 200
    assert catalogs.objects.count() > 0
    for c in catalogs.objects.all():
        assert c.title in response.content.decode()


def test_catalog_list_view(admin_client):
    baker.make('catalog.catalogs',_quantity=10)
    url = reverse('catalog:catalog_list_view')
    response = admin_client.get(url)
    assert response.status_code == 200
    assert catalogs.objects.count() > 0
    for c in catalogs.objects.all():
        assert c.title in response.content.decode()


def test_catalog_detail_view(admin_client):
    cat = baker.make('catalog.catalogs',make_m2m=True,_fill_optional=True)
    url = reverse('catalog:catalog_detail_view', kwargs={'pk': cat.id})
    response = admin_client.get(url)
    assert response.status_code == 200


def test_control_detail_view(admin_client):
    baker.make('catalog.controls',_quantity=1,make_m2m=True,_fill_optional=True)
    ctrl = controls.objects.first()
    url = reverse('catalog:control_detail_view', kwargs={'pk': ctrl.id})
    response = admin_client.get(url)
    assert response.status_code == 200


def test_model_test(admin_client):
    test_obj = baker.make(tests, _fill_optional=True)
    test_obj.catalog_uuid = str(uuid.uuid4())
    test_obj.save()
    assert test_obj.__str__() == test_obj.expression


def catalog_model_test():
    test_catalog = baker.make('catalog.catalogs', make_m2m=True, _fill_optional=True)
    assert catalogs.objects.filter(pk=test_catalog.id).exists()


def test_param_model():
    param_obj = baker.make('catalog.params',make_m2m=True,_fill_optional=True)
    assert param_obj.param_id in param_obj.get_form()
    param_obj.select = 'pick one'
    param_obj.save()
    assert "<select" in param_obj.get_form()
    param_obj.how_many = "one-or-more"
    param_obj.save()
    assert "<select multiple" in param_obj.get_form()
    assert param_obj.param_id in param_obj.to_html()


def test_parts_model():
    parts_obj = baker.make('catalog.parts',make_m2m=True,_fill_optional=True)
    assert type(parts_obj.to_html()) is str


def test_controls_model():
    ctrl = baker.make('catalog.controls',_fill_optional=True,make_m2m=True)
    assert ctrl.__str__() == ctrl.control_class + " " + ctrl.control_id + " " + ctrl.title
    assert ctrl.set_sort_id() == False
    assert type(ctrl.to_html()) is str
    assert type(ctrl.to_html_short()) is str
    assert ctrl.count_controls() == (1, 5)


def test_groups_model():
    grp = baker.make('catalog.groups',_fill_optional=True,make_m2m=True)
    assert grp.__str__() == grp.group_id.upper() + " - " + grp.title + " (" + grp.group_class + ")"
    assert type(grp.to_html()) is str


@pytest.mark.slow
def test_import_catalog_view(admin_client):

    cat, _ = available_catalog_list.objects.get_or_create(catalog_uuid='74c8ba1e-5cd4-4ad1-bbfd-d888e2f6c724', link='https://raw.githubusercontent.com/usnistgov/oscal-content/main/examples/catalog/json/basic-catalog-min.json', name='Sample Security Catalog *for Demonstration* and Testing')
    url = reverse('catalog:import_catalog_view', kwargs={'catalog_id': cat.id})
    response = admin_client.get(url)
    assert response.status_code == 302