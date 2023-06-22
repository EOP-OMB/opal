from django.urls import reverse

import pytest

from model_bakery import baker
# Add generators for custom field types
from model_bakery.random_gen import gen_m2m, gen_string, gen_text
baker.generators.add('common.models.ShortTextField', gen_string)
baker.generators.add('ckeditor.fields.RichTextField', gen_text)
baker.generators.add('common.models.properties_field', gen_m2m)

pytestmark = pytest.mark.django_db


# @pytest.mark.skip
def test_import_ssp_view(admin_client):
    url = reverse('ssp:import_ssp_view', kwargs={'ssp_file': 'ssp-example.json'})
    response = admin_client.get(url)
    assert response.status_code == 302


# @pytest.mark.skip
def test_import_ssp_view_with_existing_ssp(admin_client):
    url = reverse('ssp:import_ssp_view', kwargs={'ssp_file': 'ssp-example.json'})
    admin_client.get(url)
    # now we try to re-import the same ssp
    response = admin_client.get(url)
    assert response.status_code == 302


# @pytest.mark.skip
def test_import_ssp_view_file_not_found(admin_client):
    url = reverse('ssp:import_ssp_view', kwargs={'ssp_file': 'some_file.json'})
    response = admin_client.get(url)
    assert response.status_code == 302


def test_system_security_plan_model(admin_client):
    test_ssp = baker.make('ssp.system_security_plans',make_m2m=True,_fill_optional=True)
    assert type(test_ssp.to_html()) is str