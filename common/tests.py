from django.test import Client
from django.contrib.auth import get_user_model
from common.functions import reset_all_db, search_for_uuid, replace_hyphen, coalesce
import uuid
from model_mommy import mommy
from common.models import links, roles
from catalog.models import available_catalog_list, controls


# Create your tests here.
from django.urls import reverse


def test_index_view(db):
    c = Client()
    c.get(reverse("common:app_init"))
    url = reverse('home_page')
    response = c.get(url)
    assert response.status_code == 200


def test_db_status_view(db):
    c = Client()
    url = reverse('common:db_status')
    response = c.get(url)
    assert response.status_code == 200


def test_reset_all_db_function(db):
    reset_all_db()


def test_permalink(db):
    test_ctrl = mommy.make(controls, _fill_optional=True)
    test_ctrl.uuid = str(uuid.uuid4())
    test_ctrl.save()
    c = Client()
    url = reverse('common:permalink', kwargs={'p_uuid': str(test_ctrl.uuid)})
    resp = c.get(url)
    assert resp.status_code == 302
    uuid_str = str(uuid.uuid4())
    url = reverse('common:permalink', kwargs={'p_uuid': uuid_str})
    resp = c.get(url)
    assert resp.status_code == 404


def test_search_for_uuid_function(db):
    uuid_str = str(uuid.uuid4())
    assert search_for_uuid(uuid_str) == None
    new_link = mommy.make(links)
    assert search_for_uuid(str(new_link.uuid)) == new_link


def test_replace_hyphen_function():
    string = "this-is-a-string-with-hyphens"
    assert replace_hyphen(string) == "this_is_a_string_with_hyphens"


def test_coalesce_function():
    assert coalesce(None,"",'Something','SomethingElse') == 'Something'
    assert coalesce(None,"",None) == "N/A"


def test_app_init(db):
    c = Client()
    resp = c.get(reverse("common:app_init"))
    assert resp.status_code == 200
    user = get_user_model()
    assert user.objects.filter(is_superuser=True).exists()
    assert available_catalog_list.objects.count() == 10
    assert roles.objects.count() == 18