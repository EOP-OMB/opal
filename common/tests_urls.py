import pytest
from django.test import Client
from django.urls import reverse




basic_urls = ['catalog:catalog_index_view','catalog:ajax_load_controls','catalog:ajax_load_params','catalog:ajax_load_statements','catalog:catalog_list_view','common:auth_view','common:db_status','common:create_base64','common:base64_list','common:add_resource_view','component:component_list_view','component:components_form_view','ctrl_profile:profile_list_view','ctrl_profile:create_profile_view','ssp:ssp_list_view','ssp:add_new_ssp_view']

c = Client()
for l in basic_urls:
    url = reverse(l)
    response = c.get(path=url)
    print(response)



# /catalog/<int:pk>	catalog.views.catalog_detail_view	catalog:catalog_detail_view
# /catalog/control/<int:pk>	catalog.views.control_detail_view	catalog:control_detail_view
# /catalog/import/<str:catalog_id>	catalog.views.import_catalog_view	catalog:import_catalog_view
# /celery-progress/<task_id>/	celery_progress.views.get_progress	celery_progress:task_status
# /common/f/detail/<int:pk>	common.views.base64_detail_view	common:base64_detail
# /common/f/render/<int:pk>	common.views.base64_render_view	common:base64_render
# /common/p/<str:p_uuid>	common.views.permalink_view	common:permalink_view
# /component/<int:pk>	component.views.component_detail_view	component:component_detail_view
# /profiles/<int:pk>	ctrl_profile.views.profile_detail_view	ctrl_profile:profile_detail_view
# /ssp/<int:pk>	ssp.views.ssp_detail_view	ssp:ssp_detail_view
# /ssp/import/<str:ssp_file>	ssp.views.import_ssp_view	ssp:import_ssp_view