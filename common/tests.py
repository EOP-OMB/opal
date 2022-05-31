from django.test import Client
from .functions import reset_all_db, search_for_uuid, replace_hyphen, coalesce
import uuid
from .factory import linksFactory
from .models import links


# Create your tests here.
from django.urls import reverse


def test_index_view(db):
    c = Client()
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


def test_search_for_uuid_function(db):
    uuid_str = str(uuid.uuid4())
    search_for_uuid(uuid_str) == None
    new_link = linksFactory()
    search_for_uuid(str(new_link.uuid)) == new_link


def test_replace_hyphen_function():
    string = "this-is-a-string-with-hyphens"
    assert replace_hyphen(string) == "this_is_a_string_with_hyphens"


def test_coalesce_function():
    assert coalesce(None,"",'Something','SomethingElse') == 'Something'
    assert coalesce(None,"",None) == "N/A"