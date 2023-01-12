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

from ssp.views import ssp_list_view, ssp_detail_view, import_ssp_view, add_new_ssp_view, ssp_wizard

app_name = 'ssp'
urlpatterns = [
    path('', ssp_list_view.as_view(), name='ssp_list_view'),
    path('<int:pk>', ssp_detail_view.as_view(), name='ssp_detail_view'),
    path('import/<str:ssp_file>', import_ssp_view, name='import_ssp_view'),
    path('add/', add_new_ssp_view, name='add_new_ssp_view'),
    path('wizard', ssp_wizard.as_view(), name='ssp_wizard'),
    ]
