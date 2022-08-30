import pytest
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db

@pytest.mark.django_db
def test_my_user():
    me = User.objects.get(username='admin')
    assert me.is_superuser
