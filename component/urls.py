from django.urls import path
from component.views import component_list_view, component_detail_view

app_name = 'component'
urlpatterns = [
    path('', component_list_view, name='component_list_view'),
    path('<int:pk>', component_detail_view.as_view(), name='component_detail_view'),
    ]
