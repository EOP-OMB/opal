import os

from ssp.models import system_security_plans
from django.urls import reverse
from django.conf import settings
import pytest

pytestmark = pytest.mark.django_db

# from ssp.views import import_ssp

# Create your tests here.


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
    test_ssp = system_security_plans.objects.get(uuid='cff8385f-108e-40a5-8f7a-82f3dc0eaba8')
    assert test_ssp.to_html() == "<h1>Enterprise Logging and Auditing System Security Plan</h1><h2>Metadata</h2><div class='card'  style=''><div class='card-body'><p class='card-text'>\n<div style='margin-left: 0px;'><li>Document Title: Enterprise Logging and Auditing System Security Plan</li>\n<li>Last Modified Timestamp: 2021-06-08T17:57:28.355446+00:00</li>\n<li>Document Version: 1.0</li>\n<li>OSCAL Version: 1.0.0</li>\n<li>Parties (organizations or persons) <a href='/admin/common/metadata/add/'>(Add)</a>:</li>\n\n<div style='margin-left: 20px;'><li>Party Type: organization</li>\n<li>Party Name: Enterprise Asset Owners</li>\n</ul>\n</div>\n<div style='margin-left: 20px;'><li>Party Type: organization</li>\n<li>Party Name: Enterprise Asset Administrators</li>\n</ul>\n</div>\n<div style='margin-left: 20px;'><li>Party Type: organization</li>\n<li>Party Name: Legal Department</li>\n</ul>\n</div>\n<div style='margin-left: 20px;'><li>Party Type: organization</li>\n<li>Party Name: IT Department</li>\n</ul>\n</div>\n<div style='margin-left: 20px;'><li>Party Type: organization</li>\n<li>Party Name: Acme Corp</li>\n</ul>\n</div></ul>\n</div></p></div></div><h2>System Characteristics</h2><div class='card'  style=''><div class='card-body'><p class='card-text'>\n<div style='margin-left: 0px;'><li>System Name - Full: Enterprise Logging and Auditing System</li>\n<li>System Name - Short: None</li>\n<li>System Description: This is an example of a system that provides enterprise logging and log auditing capabilities.</li>\n<li>Security Sensitivity Level: moderate</li>\n<li>Security Impact Level: None</li>\n<li>Security Objective: Confidentiality: None</li>\n<li>Security Objective: Integrity: None</li>\n<li>Security Objective: Availability: None</li>\n<li>Status: None</li>\n<li>Authorization Boundary: \n<div style='margin-left: 20px;'><li>Authorization Boundary Description: The description of the authorization boundary would go here.</li>\n</ul>\n</div></li>\n<li>Alternative System Identifier <a href='/admin/ssp/system_characteristics/add/'>(Add)</a>:</li>\n\n<div style='margin-left: 20px;'></ul>\n</div><li>Properties <a href='/admin/ssp/system_characteristics/add/'>(Add)</a>:</li>\n\n<div style='margin-left: 20px;'><li>Property Name: deployment-model</li>\n<li>Property Namespace: https://csrc.nist.gov/ns/oscal</li>\n<li>Property Value: private</li>\n</ul>\n</div>\n<div style='margin-left: 20px;'><li>Property Name: service-models</li>\n<li>Property Namespace: https://csrc.nist.gov/ns/oscal</li>\n<li>Property Value: iaas</li>\n</ul>\n</div><li>System Information <a href='/admin/ssp/system_characteristics/add/'>(Add)</a>:</li>\n\n<div style='margin-left: 20px;'><li>Information Type <a href='/admin/ssp/systems_information/add/'>(Add)</a>:</li>\n<div class='card shadow mb-4'>\n<!-- Card Header - Accordion -->\n<a href='#collapseCard-b1d7b4ca-71fe-488d-8625-e1b2b5226c06' class='d-block card-header py-3' data-toggle='collapse' role='button' aria-expanded='false' aria-controls='collapseCardExample'><h6 class='m-0 font-weight-bold text-primary'>System and Network Monitoring</h6>\nConfidentiality: fips-199-moderate Availability: fips-199-low Integrity: fips-199-moderate </a>\n<!-- Card Content - Collapse -->\n<div class='collapse' id='collapseCard-b1d7b4ca-71fe-488d-8625-e1b2b5226c06' aria-expanded='false' style=''>\n<div class='card-body'>\nConfidentiality: base: fips-199-moderate, selected: fips-199-moderate, Justification: Not Adjusted<br>\nAvailability: base: fips-199-low, selected: fips-199-low, Justification: Not Adjusted<br>\nIntegrity: base: fips-199-moderate, selected: fips-199-moderate, Justification: Not Adjusted<br>\nThis system maintains historical logging and auditing information for all client devices connected to this system.\n</div>\n</div>\n</div>\n</ul>\n</div></ul>\n</div></p></div></div><h2>System Implementation</h2><div class='card'  style=''><div class='card-body'><p class='card-text'><div><h2>Components</h2>\n<ul><li><a href='/component/2'>Configuration Management Guidance ()</a> Implements: []</li>\n<li><a href='/component/3'>Enterprise Logging, Monitoring, and Alerting Policy ()</a> Implements: []</li>\n<li><a href='/component/4'>Inventory Management Process ()</a> Implements: []</li>\n<li><a href='/component/5'>Logging Server ()</a> Implements: []</li>\n<li><a href='/component/7'>System Integration Process ()</a> Implements: []</li>\n<li>None</li>\n</ul>\n<h2>Inventory</h2>\n<ul><li>\n<div style='margin-left: 0px;'><li>Inventory Item Description: The logging server.</li>\n<li>Properties <a href='/admin/ssp/inventory_items/add/'>(Add)</a>:</li>\n<li>Responsible Parties <a href='/admin/ssp/inventory_items/add/'>(Add)</a>:</li>\n<li>Implemented Components <a href='/admin/ssp/inventory_items/add/'>(Add)</a>:</li>\n</ul>\n</div></li>\n<li>None</li>\n</ul>\n<h2>Users</h2>\n<ul><li>\n<div style='margin-left: 0px;'><li>User Title: System Administrator</li>\n<li>Properties <a href='/admin/ssp/users/add/'>(Add)</a>:</li>\n<li>User Role(s) <a href='/admin/ssp/users/add/'>(Add)</a>:</li>\n</ul>\n</div></li>\n<li>\n<div style='margin-left: 0px;'><li>User Title: Audit Team</li>\n<li>Properties <a href='/admin/ssp/users/add/'>(Add)</a>:</li>\n<li>User Role(s) <a href='/admin/ssp/users/add/'>(Add)</a>:</li>\n</ul>\n</div></li>\n<li>\n<div style='margin-left: 0px;'><li>User Title: Legal Department</li>\n<li>Properties <a href='/admin/ssp/users/add/'>(Add)</a>:</li>\n<li>User Role(s) <a href='/admin/ssp/users/add/'>(Add)</a>:</li>\n</ul>\n</div></li>\n<li>None</li>\n</ul></div></p></div></div><h2>Control Implementation</h2><div class='card'  style=''><div class='card-body'><p class='card-text'><div class='control_implementation'><h3>This is the control implementation for the system.</h3><div class='implemented_requirement'><a id=s1.1.1><h4>S1.1.1 - Information security roles and responsibilities ()</h4>All information security responsibilities should be defined and allocated.\n\nA value has been assigned to {{ insert: param, s1.1.1-prm11 }}.\n\nA cross link has been established with a choppy syntax: [(choppy)](#s1.2).<br>\n<h5>Guidance</h5><p></p><div><strong>Related Controls:</strong><br></div><p><strong>References:</strong> </p></div></div></p></div></div><h2>Back Matter</h2><div class='card'  style=''><div class='card-body'><p class='card-text'></p></div></div>"