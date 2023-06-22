import uuid
from django.urls import reverse
from catalog.models import catalogs, available_catalog_list, tests, params, parts, controls
from common.models import props

import pytest

from model_bakery import baker
# Add generators for custom field types
from model_bakery.random_gen import gen_m2m, gen_string, gen_text
baker.generators.add('common.models.ShortTextField', gen_string)
baker.generators.add('ckeditor.fields.RichTextField', gen_text)
baker.generators.add('common.models.properties_field', gen_m2m)

pytestmark = pytest.mark.django_db




@pytest.fixture(scope='module', autouse=True)
def load_fixtures():
    baker.make('catalog.catalogs',_quantity=10)
    baker.make('catalog.controls',_quantity=10,make_m2m=True,_fill_optional=True)


def test_catalog_index_view(admin_client):
    # baker.make('catalog.catalogs',_quantity=10)
    url = reverse('catalog:catalog_index_view')
    response = admin_client.get(url)
    assert response.status_code == 200
    assert catalogs.objects.count() > 0
    for c in catalogs.objects.all():
        assert c.title in response.content.decode()


def test_catalog_list_view(admin_client):
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
    ctrl = controls.objects.first()
    url = reverse('catalog:control_detail_view', kwargs={'pk': ctrl.id})
    response = admin_client.get(url)
    assert response.status_code == 200


def test_load_controls_view(admin_client):
    cat = baker.make('catalog.catalogs',make_m2m=True,_fill_optional=True)
    url = reverse('catalog:ajax_load_controls') + '?catalog=' + str(cat.id)
    response = admin_client.get(url)
    assert response.status_code == 200


def test_load_statements_view(admin_client):
    ctrl = controls.objects.first()
    url = reverse('catalog:ajax_load_controls') + '?control=' + str(ctrl.id)
    response = admin_client.get(url)
    assert response.status_code == 200


@pytest.mark.slow
def test_import_catalog_view(admin_client):

    cat, created = available_catalog_list.objects.get_or_create(catalog_uuid='74c8ba1e-5cd4-4ad1-bbfd-d888e2f6c724', link='https://raw.githubusercontent.com/usnistgov/oscal-content/main/examples/catalog/json/basic-catalog-min.json', name='Sample Security Catalog *for Demonstration* and Testing')
    url = reverse('catalog:import_catalog_view', kwargs={'catalog_id': cat.id})
    response = admin_client.get(url)
    assert response.status_code == 302
    # assert catalogs.objects.filter(metadata__title='NIST Special Publication 800-53 Revision 5 MODERATE IMPACT BASELINE').exists()
    # assert profiles.objects.filter(metadata__title='NIST Special Publication 800-53 Revision 5 MODERATE IMPACT BASELINE').exists()


def test_load_controls(admin_client):
    cat = catalogs.objects.first()
    url = reverse('catalog:ajax_load_controls') + '?catalog=' + str(cat.id)
    response = admin_client.get(url)
    assert response.status_code == 200


def test_load_statements(admin_client):
    ctrl = controls.objects.first()
    url = reverse('catalog:ajax_load_statements') + '?control=' + str(ctrl.id)
    response = admin_client.get(url)
    assert response.status_code == 200


def test_load_params(admin_client):
    ctrl = controls.objects.first()
    url = reverse('catalog:ajax_load_params') + '?control=' + str(ctrl.id)
    response = admin_client.get(url)
    assert response.status_code == 200


def test_model_test(admin_client):
    test_obj = baker.make(tests, _fill_optional=True)
    test_obj.catalog_uuid = str(uuid.uuid4())
    test_obj.save()
    assert test_obj.__str__() == test_obj.expression


def get_test_param():
    test_param = params.objects.get(uuid='6b967542-b19b-4d27-bf32-a574611f6151')
    return test_param


def test_props_model():
    param_obj = params.objects.create()
    param_obj.param_id = 'test_param_1'
    param_obj.label = 'Test Param 1'
    param_obj.usage = 'To test the Param model'
    param_obj.how_many = 'one'
    param_obj.choice = 'option a\noption b\noption c'
    assert param_obj.get_form() == "<tr><td></td><td>test_param_1</td><td><input type=text value='' name='test_param_1'></td></tr>"
    param_obj.select = 'pick one'
    assert param_obj.get_form() == "<tr><td></td><td>test_param_1</td><td><select name='test_param_1'><option>option a</option><option>option b</option><option>option c</option></select></td></tr>"
    param_obj.how_many = "one-or-more"
    assert param_obj.get_form() == "<tr><td></td><td>test_param_1</td><td><select multiple name='test_param_1'><option>option a</option><option>option b</option><option>option c</option></select></td></tr>"
    assert param_obj.to_html() == '<td>test_param_1</td><td>Test Param 1</td><td>'


def test_parts_model():
    parts_obj = parts.objects.create(part_id='part_1', name='item', title='A test part', prose='')
    props_obj = props.objects.create(name='label', value='value')
    parts_obj.props.add(props_obj.id)
    parts_obj.prose = "Some text here"
    assert parts_obj.to_html() == 'value Some text here<br>\n'
    child_parts_obj = parts.objects.create(part_id='child_part_1', name='guidance', title='A test part')
    parts_obj.sub_parts.add(child_parts_obj.id)
    assert child_parts_obj.get_root_part() == parts_obj
    assert parts_obj.get_all_parts() == [
        parts_obj,
        child_parts_obj]
    assert parts_obj.get_control is None
    assert parts_obj.__str__() == parts_obj.part_id
    parts_obj.part_id = ''
    assert parts_obj.__str__() == parts_obj.title
    parts_obj.title = ''
    assert parts_obj.__str__() == parts_obj.name
    parts_obj.name = ''
    assert parts_obj.__str__() == parts_obj.prose[
                                  0:100]
    parts_obj.prose = ''
    assert parts_obj.__str__() == "Part: %s" % str(parts_obj.uuid)


def test_controls_model():
    ctrl = baker.make('catalog.controls',_fill_optional=True,make_m2m=True)
    assert ctrl.__str__() == ctrl.control_class + " " + ctrl.control_id + " " + ctrl.title
    assert ctrl.set_sort_id() == False
    assert type(ctrl.to_html()) is str
    assert type(ctrl.to_html_short()) is str
    assert ctrl.count_controls() == (1, 0)
    assert ctrl.list_all_controls() == [ctrl]


def test_groups_model():
    grp = baker.make('catalog.groups',_fill_optional=True,make_m2m=True)
    assert grp.__str__() == grp.group_id.upper() + " - " + grp.title + " (" + grp.group_class + ")"
    assert type(grp.to_html()) is str
    # assert grp.count_controls() == (2, 0)
    # assert grp.list_all_controls() == list(controls.objects.filter(control_id__in=['s1.1.1', 's1.1.2']).all())
