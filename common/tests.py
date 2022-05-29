from django.test import Client

from .models import *


# Create your tests here.

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
