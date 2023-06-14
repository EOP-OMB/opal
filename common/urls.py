"""opal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from common.views import permalink_view, database_status_view, auth_view, base64_list_view, base64_detail_view, upload_file, add_resource_view

app_name = 'common'
urlpatterns = [path('p/<str:p_uuid>', permalink_view, name='permalink'),
               path('db_status/', database_status_view, name='db_status'),
               path('auth/', auth_view, name='auth_view'),
               path('f/list', base64_list_view.as_view(), name='base64_list'),
               path('f/detail/<int:pk>', base64_detail_view, name='base64_detail'),
               path('f/add', upload_file, name='upload_file'),
               # path('f/render/<int:pk>', base64_render_view, name='base64_render'),
               path('r/add', add_resource_view, name='add_resource_view')
               ]
