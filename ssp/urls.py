"""OSCALweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django_filters.views import FilterView
from ssp.views import *

app_name = 'ssp'
urlpatterns = [
    path('nist/', nist_control_list_view.as_view(), name='nist_control_list_view'),
    path('nist/<int:pk>', nist_control_detail_view.as_view(), name='nist_control_detail_view'),
    # path('control/', system_control_list_view.as_view(), name='system_control_list_view'),
    path('control/', FilterView.as_view(filterset_class=system_control_list_view_filter,
                                        template_name='ssp/system_control_list.html'), name='system_control_list_view'),
    path('control/<int:pk>', system_control_detail_view.as_view(), name='system_control_detail_view'),
    path('attachments', attachment_list_view.as_view(), name='attachment_list_view'),
    path('links', link_list_view.as_view(), name='link_list_view'),
    path('', system_security_plan_list_view.as_view(), name='list_system_security_planView'),
    path('<int:pk>', system_security_plan_detail_view.as_view(), name='system_security_plan_detail_view'),
    path('new/', ssp_new, name='ssp_new'),
    path('<int:pk>/edit/', ssp_edit, name='ssp_edit'),
    path('sc/<int:pk>/edit', system_control_edit, name='system_control_edit'),
    path('catalog/', import_catalog, name='import_catalog'),
    path('system-user-new/<int:sspid>/<int:roleid>/', system_user_new, name='system_user_new'),
    path('oscal-json/<str:objurl>/<int:objid>', oscal_json, name='oscal_json'),
    path('clone_control/<int:ssp>/<int:control>/', clone_system_control, name='clone_control')
]
