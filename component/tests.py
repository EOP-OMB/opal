import pytest

import json

from common.models import metadata
from catalog.models import catalogs, controls
from ctrl_profile.models import profiles, imports
from component.models import by_components, components, implemented_requirements, statements
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


# def test_create_component_statement(db, load_sample_catalog):
#     c = Client()
#     url = reverse('component:create_component_statement')
#     response = c.get(url)
#     assert response.status_code == 200
#
#     #test loading with catalog_id selected
#     test_catalog = catalogs.objects.first()
#     url = reverse('component:create_component_statement')
#     url += '?catalog_id=%s' % test_catalog.id
#     response = c.get(url)
#     assert response.status_code == 200
#     assert response.content.decode().find(test_catalog.metadata.title) != -1
#
#     test_ctrl = controls.objects.first()
#     url = reverse('component:create_component_statement')
#     url += '?ctrl_id=%s' % test_ctrl.id
#     response = c.get(url)
#     assert response.status_code == 200
#     assert response.content.decode().find(test_ctrl.title) != -1
#
#     test_comp = components.objects.first()
#     stmt_list = test_ctrl.get_all_parts()
#     stmt_id_list = []
#     for s in stmt_list:
#         if s.name in ["item", "statement"]:
#             stmt_id_list.append(s.id)
#     comp_id = test_comp.id
#     impl_description = 'This is a description of how the control is implement'
#     impl_status = 'implemented'
#     ctrl_id = test_ctrl.id
#     statement_list = stmt_id_list
#
#     c.post(reverse('component:create_component_statement'), data={'component_uuid': comp_id, 'description': impl_description, 'implementation_status': impl_status, 'controls': ctrl_id, 'statements': statement_list })
#     assert by_components.objects.filter(component_uuid=comp_id, description=impl_description, implementation_status=impl_status).exists()
#     new_bc = by_components.objects.get(component_uuid=comp_id, description=impl_description, implementation_status=impl_status)
#     assert statements.objects.filter(by_components=new_bc.id).exists()
#     new_stmt = statements.objects.get(new_bc.id)
#     new_implemented_requirement = implemented_requirements.objects.get(control_id=ctrl_id)
#     assert new_implemented_requirement.statements.by_components.count == len(stmt_id_list)
