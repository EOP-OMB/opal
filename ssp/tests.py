from ssp.models import *
from django.test import Client
from django.urls import reverse


# Create your tests here.

# @pytest.mark.skip
def test_import_ssp_view(db):
    c = Client()
    url = reverse('ssp:import_ssp_view', kwargs={'ssp_file': 'ssp-example.json'})
    response = c.get(url)
    assert response.status_code == 302
    assert system_security_plans.objects.filter(metadata__title='Enterprise Logging and Auditing System Security Plan').exists()


# @pytest.mark.skip
def test_import_ssp_view_with_existing_ssp(db):
    c = Client()
    url = reverse('ssp:import_ssp_view', kwargs={'ssp_file': 'ssp-example.json'})
    c.get(url)
    # now we try to re-import the same ssp
    response = c.get(url)
    assert response.status_code == 302
    assert system_security_plans.objects.filter(metadata__title='Enterprise Logging and Auditing System Security Plan').exists()


# @pytest.mark.skip
def test_import_ssp_view_file_not_found(db):
    c = Client()
    url = reverse('ssp:import_ssp_view', kwargs={'ssp_file': 'some_file.json'})
    response = c.get(url)
    assert response.status_code == 302
