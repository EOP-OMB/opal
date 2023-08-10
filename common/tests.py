from common.functions import search_for_uuid, replace_hyphen, coalesce
import uuid
from common.models import links
from django.urls import reverse

import pytest

from model_bakery import baker
# Add generators for custom field types
from model_bakery.random_gen import gen_m2m, gen_string, gen_text
baker.generators.add('common.models.ShortTextField', gen_string)
baker.generators.add('ckeditor.fields.RichTextField', gen_text)
baker.generators.add('common.models.properties_field', gen_m2m)

pytestmark = pytest.mark.django_db


def test_index_view(admin_client):
    url = reverse('home_page')
    response = admin_client.get(url)
    assert response.status_code == 200


def test_db_status_view(admin_client):
    url = reverse('common:db_status')
    response = admin_client.get(url)
    assert response.status_code == 200


def test_permalink(admin_client):
    test_ctrl = baker.make('catalog.controls', _fill_optional=True)
    test_url = reverse('common:permalink', kwargs={'p_uuid': str(test_ctrl.uuid)})
    resp = admin_client.get(test_url)
    assert resp.status_code == 302
    uuid_str = str(uuid.uuid4())
    test_url = reverse('common:permalink', kwargs={'p_uuid': uuid_str})
    resp = admin_client.get(test_url)
    assert resp.status_code == 404


def test_search_for_uuid_function(db):
    uuid_str = str(uuid.uuid4())
    assert search_for_uuid(uuid_str) is None
    new_link = baker.make(links)
    assert search_for_uuid(str(new_link.uuid)) == new_link


def test_replace_hyphen_function():
    string = "this-is-a-string-with-hyphens"
    assert replace_hyphen(string) == "this_is_a_string_with_hyphens"


def test_coalesce_function():
    assert coalesce(None, "", 'Something', 'SomethingElse') == 'Something'
    assert coalesce(None, "", None) == "N/A"
