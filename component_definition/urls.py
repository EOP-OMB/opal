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
from .views import *

app_name = 'component'
urlpatterns = [path('', component_list_view.as_view(), name='component_list_view'),
    path('<int:pk>', component_detail_view.as_view(), name='component_detail_view'),
    path('new', create_component_view.as_view(), name='create_component_view'),
    path('parameter/new/<int:param_id>', create_parameter_view.as_view(), name='create_parameter_view'), path(
        'implemented_requirements/new', create_implemented_requirements_view.as_view(),
        name='create_implemented_requirements_view'
        ), path('requirement/new/<int:control_id>', implemented_requirements_form_view, name='new_requirement')]
