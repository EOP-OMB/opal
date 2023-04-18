import uuid
# noinspection PyPackageRequirements
import pytest
from django.urls import reverse
from model_bakery import baker

from catalog.models import catalogs, available_catalog_list, tests, params, parts, controls, groups
from catalog.views import import_catalog_task
from common.models import props

pytestmark = pytest.mark.django_db


# Create your tests here.
# @pytest.fixture(scope='function', autouse=True)
# def get_sample_catalog_id(db):
#     host = settings.HOST_NAME
#     item = {}
#     new_catalog = import_catalog_task(item, host, test=True)
#     return new_catalog.id


# def get_sample_catalog_id():
#     if catalogs.objects.count() == 0:
#         import_catalog_task(test=True)
#     sample_catalog = catalogs.objects.first()
#     return sample_catalog.id

def get_test_catalog():
    test_catalog = catalogs.objects.get(uuid='74c8ba1e-5cd4-4ad1-bbfd-d888e2f6c724')
    return test_catalog

def get_test_control():
    ctrl = controls.objects.get(uuid='c917d796-1b5f-4994-9366-d4eadd05ba72')
    return ctrl

def test_catalog_index_view(admin_client):
    url = reverse('catalog:catalog_index_view')
    response = admin_client.get(url)
    assert response.status_code == 200


def test_catalog_list_view(admin_client):
    url = reverse('catalog:catalog_list_view')
    response = admin_client.get(url)
    assert response.status_code == 200


def test_catalog_detail_view(admin_client):
    cat = get_test_catalog()
    url = reverse('catalog:catalog_detail_view', kwargs={'pk': cat.id})
    response = admin_client.get(url)
    assert response.status_code == 200


def test_control_detail_view(admin_client):
    ctrl = get_test_control()
    url = reverse('catalog:control_detail_view', kwargs={'pk': ctrl.id})
    response = admin_client.get(url)
    assert response.status_code == 200

def test_load_controls_view(admin_client):
    cat = get_test_catalog()
    url = reverse('catalog:ajax_load_controls') + '?catalog=' + str(cat.id)
    response = admin_client.get(url)
    assert response.status_code == 200


def test_load_statements_view(admin_client):
    ctrl = get_test_control()
    url = reverse('catalog:ajax_load_controls') + '?control=' + str(ctrl.id)
    response = admin_client.get(url)
    assert response.status_code == 200


@pytest.mark.slow
def test_import_catalog_view(admin_client):
    url = reverse('catalog:import_catalog_view', kwargs={'catalog_id': available_catalog_list.objects.first().id})
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
    ctrl = get_test_control()
    url = reverse('catalog:ajax_load_statements') + '?control=' + str(ctrl.id)
    response = admin_client.get(url)
    assert response.status_code == 200


def test_load_params(admin_client):
    ctrl = get_test_control()
    url = reverse('catalog:ajax_load_params') + '?control=' + str(ctrl.id)
    response = admin_client.get(url)
    assert response.status_code == 200


def test_model_test(admin_client):
    test_obj = baker.make(tests, _fill_optional=True)
    test_obj.uuid = str(uuid.uuid4())
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
    ctrl = controls.objects.get(control_id='s1.1.1')
    assert ctrl.__str__() == ' s1.1.1 Information security roles and responsibilities'
    assert ctrl.set_sort_id() == False
    assert ctrl.to_html() == '<a id=s1.1.1><h4>S1.1.1 - Information security roles and responsibilities ()</h4>All information security responsibilities should be defined and allocated.\n\nA value has been assigned to {{ insert: param, s1.1.1-prm11 }}.\n\nA cross link has been established with a choppy syntax: [(choppy)](#s1.2).<br>\n<h5>Guidance</h5><p></p>&nbsp;&nbsp;Allocation of information security responsibilities should be done in accordance with the information security policies. Responsibilities for the protection of individual assets and for carrying out specific information security processes should be identified. Responsibilities for information security risk management activities and in particular for acceptance of residual risks should be defined. These responsibilities should be supplemented, where necessary, with more detailed guidance for specific sites and information processing facilities. Local responsibilities for the protection of assets and for carrying out specific security processes should be defined.<br>\n&nbsp;&nbsp;Individuals with allocated information security responsibilities may delegate security tasks to others. Nevertheless they remain accountable and should determine that any delegated tasks have been correctly performed.<br>\n&nbsp;&nbsp;Areas for which individuals are responsible should be stated. In particular the following should take place:\n\n1. the assets and information security processes should be identified and defined;\n1. the entity responsible for each asset or information security process should be assigned and the details of this responsibility should be documented;\n1. authorization levels should be defined and documented;\n1. to be able to fulfil responsibilities in the information security area the appointed individuals should be competent in the area and be given opportunities to keep up to date with developments;\n1. coordination and oversight of information security aspects of supplier relationships should be identified and documented.\n<br>\n<div><strong>Related Controls:</strong><br></div><p><strong>References:</strong> </p>'
    assert ctrl.to_html_short() == '<a id=s1.1.1><h4>S1.1.1 - Information security roles and responsibilities ()</h4>All information security responsibilities should be defined and allocated.\n\nA value has been assigned to {{ insert: param, s1.1.1-prm11 }}.\n\nA cross link has been established with a choppy syntax: [(choppy)](#s1.2).<br>\n&nbsp;&nbsp;Allocation of information security responsibilities should be done in accordance with the information security policies. Responsibilities for the protection of individual assets and for carrying out specific information security processes should be identified. Responsibilities for information security risk management activities and in particular for acceptance of residual risks should be defined. These responsibilities should be supplemented, where necessary, with more detailed guidance for specific sites and information processing facilities. Local responsibilities for the protection of assets and for carrying out specific security processes should be defined.<br>\n&nbsp;&nbsp;Individuals with allocated information security responsibilities may delegate security tasks to others. Nevertheless they remain accountable and should determine that any delegated tasks have been correctly performed.<br>\n&nbsp;&nbsp;Areas for which individuals are responsible should be stated. In particular the following should take place:\n\n1. the assets and information security processes should be identified and defined;\n1. the entity responsible for each asset or information security process should be assigned and the details of this responsibility should be documented;\n1. authorization levels should be defined and documented;\n1. to be able to fulfil responsibilities in the information security area the appointed individuals should be competent in the area and be given opportunities to keep up to date with developments;\n1. coordination and oversight of information security aspects of supplier relationships should be identified and documented.\n<br>\n'
    assert ctrl.count_controls() == (
        1,
        0)
    assert ctrl.list_all_controls() == [
        ctrl]


def test_groups_model():
    grp = groups.objects.get(group_id='s1')
    assert grp.__str__() == 'S1 - Organization of Information Security ()'
    assert grp.to_html() == "<h3>S1 - Organization of Information Security ()</h3>\n<div style='margin-left: 0px;'><li>Property Name: label</li>\n<li>Property Value: 1</li>\n</ul>\n</div><h3>S1.1 - Internal Organization ()</h3>\n<div style='margin-left: 0px;'><li>Property Name: label</li>\n<li>Property Value: 1.1</li>\n</ul>\n</div><a id=s1.1.1><h4>S1.1.1 - Information security roles and responsibilities ()</h4>All information security responsibilities should be defined and allocated.\n\nA value has been assigned to {{ insert: param, s1.1.1-prm11 }}.\n\nA cross link has been established with a choppy syntax: [(choppy)](#s1.2).<br>\n<h5>Guidance</h5><p></p>&nbsp;&nbsp;Allocation of information security responsibilities should be done in accordance with the information security policies. Responsibilities for the protection of individual assets and for carrying out specific information security processes should be identified. Responsibilities for information security risk management activities and in particular for acceptance of residual risks should be defined. These responsibilities should be supplemented, where necessary, with more detailed guidance for specific sites and information processing facilities. Local responsibilities for the protection of assets and for carrying out specific security processes should be defined.<br>\n&nbsp;&nbsp;Individuals with allocated information security responsibilities may delegate security tasks to others. Nevertheless they remain accountable and should determine that any delegated tasks have been correctly performed.<br>\n&nbsp;&nbsp;Areas for which individuals are responsible should be stated. In particular the following should take place:\n\n1. the assets and information security processes should be identified and defined;\n1. the entity responsible for each asset or information security process should be assigned and the details of this responsibility should be documented;\n1. authorization levels should be defined and documented;\n1. to be able to fulfil responsibilities in the information security area the appointed individuals should be competent in the area and be given opportunities to keep up to date with developments;\n1. coordination and oversight of information security aspects of supplier relationships should be identified and documented.\n<br>\n<div><strong>Related Controls:</strong><br></div><p><strong>References:</strong> </p><a id=s1.1.2><h4>S1.1.2 - Segregation of duties ()</h4>Conflicting duties and areas of responsibility should be segregated to reduce opportunities for unauthorized or unintentional modification or misuse of the organization’s assets.<br>\n<h5>Guidance</h5><p></p>&nbsp;&nbsp;Care should be taken that no single person can access, modify or use assets without authorization or detection. The initiation of an event should be separated from its authorization. The possibility of collusion should be considered in designing the controls.<br>\n&nbsp;&nbsp;Small organizations may find segregation of duties difficult to achieve, but the principle should be applied as far as is possible and practicable. Whenever it is difficult to segregate, other controls such as monitoring of activities, audit trails and management supervision should be considered.<br>\n<div><strong>Related Controls:</strong><br></div><p><strong>References:</strong> </p>"
    assert grp.count_controls() == (
        2,
        0)
    assert grp.list_all_controls() == list(controls.objects.filter(control_id__in=[
        's1.1.1',
        's1.1.2']).all())
