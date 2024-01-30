import pytest
from django.urls import reverse

from model_bakery import baker
# Add generators for custom field types
from model_bakery.random_gen import gen_m2m, gen_string, gen_text
baker.generators.add('common.models.ShortTextField', gen_string)
baker.generators.add('ckeditor.fields.RichTextField', gen_text)
baker.generators.add('common.models.properties_field', gen_m2m)

pytestmark = pytest.mark.django_db


def test_component_model():
    test_component = baker.make('component.components', make_m2m=True, _fill_optional=True)
    assert type(test_component.to_html()) is str


def test_component_list_view(admin_client):
    baker.make('component.components',make_m2m=True, _fill_optional=True, _quantity=3)
    baker.make('catalog.controls', make_m2m=True, _fill_optional=True)
    ctrl_with_implementations = baker.make('component.components',make_m2m=True, _fill_optional=True)
    baker.make('component.control_implementations', make_m2m=True, _fill_optional=True, component=ctrl_with_implementations)

    url = reverse('component:component_list_view')
    response = admin_client.get(path=url)
    assert response.status_code == 200


def test_components_form_view(admin_client):
    url = reverse('component:component_form_view')
    response = admin_client.get(path=url)
    assert response.status_code == 200

    component_instance = baker.prepare('component.components')
    url = reverse('component:component_form_view')
    post_data = component_instance.to_dict()
    post_data['workflow_action'] = 'submit'
    response = admin_client.post(path=url, data=post_data)
    assert response.status_code == 302

def test_policy_component_form_view(admin_client):
    url = reverse('component:policy_component_form_view')
    response = admin_client.get(path=url)
    assert response.status_code == 200

    component_instance = baker.prepare('component.components')
    url = reverse('component:policy_component_form_view')
    post_data = component_instance.to_dict()
    post_data['scope'] = 'All OMB Systems'
    post_data['policy_owner'] = 'Some User'
    post_data['review_interval'] = 'Annually'
    post_data['workflow_action'] = 'submit'
    response = admin_client.post(path=url, data=post_data)
    assert response.status_code == 302

def test_cloud_service_component_form_view(admin_client):
    url = reverse('component:cloud_service_component_form_view')
    response = admin_client.get(path=url)
    assert response.status_code == 200

    component_instance = baker.prepare('component.components')
    url = reverse('component:cloud_service_component_form_view')
    post_data = component_instance.to_dict()
    post_data['url'] = 'https://test.gov'
    post_data['application_owner'] = 'Some User'
    post_data['workflow_action'] = 'submit'
    response = admin_client.post(path=url, data=post_data)
    assert response.status_code == 302