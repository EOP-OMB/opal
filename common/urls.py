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

from common.views import permalink, database_status_view, auth_view, base64_list_view, base64_detail_view, add_base64_attachment_view, base64_render_view

app_name = 'common'
urlpatterns = [path('p/<str:p_uuid>', permalink, name='permalink'),
               path('db_status/', database_status_view, name='db_status'),
               path('auth/', auth_view, name='auth_view'),
               path('f/list', base64_list_view.as_view(), name='base64_list'),
               path('f/detail/<int:pk>', base64_detail_view.as_view(), name='base64_detail'),
               path('f/add', add_base64_attachment_view, name='create_base64'),
               path('f/render/<int:pk>', base64_render_view, name='base64_render')
               ]
