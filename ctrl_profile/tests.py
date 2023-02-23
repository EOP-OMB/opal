from django.test import TestCase
from django.urls import reverse

from catalog.models import controls
from component.views import component_list_view
from ctrl_profile.models import imports, profiles
from model_bakery import baker
import pytest
# Create your tests here.

pytestmark = pytest.mark.django_db


def test_imports_model():
    imp = imports.objects.create(
        href="http://example.com/",
        import_type="catalog",
        include_all="True",
    )
    assert imp.to_html() == "<a href='http://example.com/'>Include all controls from catalog http://example.com/</a>"
    assert imp.__str__() == 'http://example.com/'
    ctrl_set = baker.prepare('catalog.controls', _quantity=5)
    imp_with_include_controls = baker.make(imports, include_controls=ctrl_set, include_all=False)
    assert imp_with_include_controls.to_html() == "<a href=''>Include only the following controls from  .<br>  ,   ,   ,   ,   </a>"
    imp_with_exclude_controls = baker.make(imports, exclude_controls=ctrl_set, include_all=False)
    assert imp_with_exclude_controls.to_html() == "<a href=''>Include all controls from   except the following.<br></a>"


def test_profiles_model():
    test_profile = profiles.objects.filter(metadata__title='Sample Security Catalog *for Demonstration* and Testing').first()
    assert test_profile.list_all_controls() == [
            controls.objects.get(control_id='s1.1.1'),
            controls.objects.get(control_id='s1.1.2'),
            controls.objects.get(control_id='s2.1.1'),
            controls.objects.get(control_id='s2.1.2')]
    assert test_profile.to_html() == '<h1>Sample Security Catalog *for Demonstration* and Testing</h1><h2>Metadata</h2>\n<div style=\'margin-left: 0px;\'><li>Remarks: The following is a short excerpt from [ISO/IEC 27002:2013](https://www.iso.org/standard/54533.html), *Information technology — Security techniques — Code of practice for information security controls*. This work is provided here under copyright "fair use" for non-profit, educational purposes only. Copyrights for this work are held by the publisher, the International Organization for Standardization (ISO).</li>\n<li>Document Title: Sample Security Catalog *for Demonstration* and Testing</li>\n<li>Publication Timestamp: 2020-02-02T15:01:04.736000+00:00</li>\n<li>Last Modified Timestamp: 2021-06-08T17:57:28.355446+00:00</li>\n<li>Document Version: 1.0</li>\n<li>OSCAL Version: 1.0.0</li>\n</ul>\n</div><hr>\n<table class=\'table table-striped\'>\n<tr><td colspan=3><h3>S1 - Organization of Information Security ()</h3></td></tr><tr><td colspan=3><h4>S1.1 - Internal Organization ()</h4></td></tr><tr><td colspan=3><h3>S2 - Access control ()</h3></td></tr><tr><td colspan=3><h4>S2.1 - Business requirements of access control ()</h4></td></tr><tr><td colspan=3><h3>Controls not in a Group</h3></td></tr></table>\n'


def test_component_list_view(admin_client):
    url = reverse('component:component_list_view')
    response = admin_client.get(path=url)
    assert response.status_code == 200



