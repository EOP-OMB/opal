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

from control_profile.views import *

app_name = 'control_profile'
urlpatterns = [path('', profile_list_view.as_view(), name='profile_list_view'),
               path('<int:pk>', profile_detail_view.as_view(), name='profile_detail_view'),
               path('new', createProfileView.as_view(), name='create_profile_view')]
