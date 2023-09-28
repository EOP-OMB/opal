from django.urls import path
from component.views import component_list_view, component_detail_view, policy_component_form_view, cloud_service_component_form_view, component_form_view

app_name = 'component'
urlpatterns = [
    path('', component_list_view, name='component_list_view'),
    path('<int:pk>', component_detail_view.as_view(), name='component_detail_view'),
    path('add/', component_form_view, name='component_form_view'),
    path('add/policy/', policy_component_form_view, name='policy_component_form_view'),
    path('add/cloud_service/', cloud_service_component_form_view, name='cloud_service_component_form_view'),
    ]
