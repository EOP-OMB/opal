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

from catalog.views import *

app_name = 'catalog'
urlpatterns = [path('', catalog_index_view, name='catalog_index_view'),
               path('list', catalog_list_view.as_view(), name='catalog_list_view'),
               path('<int:pk>', catalog_detail_view.as_view(), name='catalog_detail_view'),
               path('import/<str:catalog_link>', import_catalog_view, name='import_catalog_view'),
               path('control/<int:pk>', control_detail_view.as_view(), name='control_detail_view'), ]
