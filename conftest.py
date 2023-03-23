import pytest

from django.core.management import call_command


@pytest.fixture(scope='session',autouse=True)
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('bootstrap')
        call_command('runscript', 'sample_data.fixtures_for_testing')