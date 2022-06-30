import pytest

import common.functions
from .factory import *
import json

from common.models import metadata
from catalog.models import catalogs
from ctrl_profile.models import profiles, imports
from component.models import components
from django.test import Client
from django.urls import reverse


# Create your tests here.

@pytest.fixture(scope='module')
def load_sample_catalog(django_db_blocker):
    catalog_file = "sample_data/basic-catalog.json"
    catalog_json = json.load(open(catalog_file))
    catalog_dict = catalog_json["catalog"]
    with django_db_blocker.unblock():
        new_catalog = catalogs()
        new_catalog.import_oscal(catalog_dict)
        new_catalog.save()
        # create a new profiles for the imported catalog
        new_metadata = metadata.objects.create(title=new_catalog.metadata.title)
        new_profile = profiles.objects.create(
            metadata=new_metadata
            )
        new_profile.save()
        url = "https://test_host/" + new_catalog.get_permalink()
        new_profile.imports.add(imports.objects.create(href=url, import_type="catalog"))
        new_profile.save()
        # create components for any groups in the catalog
        for group in new_catalog.groups.all():
            new_component = components.objects.get_or_create(
                type="policy", title=group.title + " Policy",
                description="This Component Policy was automatically created durring the import of " + new_metadata.title,
                purpose="This Component Policy was automatically created durring the import of " + new_metadata.title,
                status="under-development"
                )
    return new_catalog.id

def test_create_component_statement(db, load_sample_catalog):
    c = Client()
    url = reverse('component:create_component_statement')
    response = c.get(url)
    assert response.status_code == 200

    test_profile = profiles.objects.first()
    c = Client()
    url = reverse('component:create_component_statement', kwargs={'profile_id': test_profile})
    response = c.get(url)
    assert response.status_code == 200
    assert catalogs.objects.filter(metadata__title='NIST Special Publication 800-53 Revision 5 MODERATE IMPACT BASELINE').exists()
    assert profiles.objects.filter(metadata__title='NIST Special Publication 800-53 Revision 5 MODERATE IMPACT BASELINE').exists()

    test_ctrl = controls.objects.first()
    url = reverse('component:create_component_statement', kwargs={'ctrl_id': test_ctrl})
    response = c.get(url)
    assert response.status_code == 200

    assert False
