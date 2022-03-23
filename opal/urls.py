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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from common.views import index_view

urlpatterns = [path('', index_view, name='home_page'), path('admin/', admin.site.urls),
                  path('catalog/', include('catalog.urls'), name='catalog'),
                  path('common/', include('common.urls'), name='common'),
                  path('component/', include('component_definition.urls'), name='component'),
                  path('profiles/', include('control_profile.urls'), name='control_profile'),
                  path('ssp/', include('ssp.urls'), name='ssp'), ] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    ) + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )

handler404 = 'common.views.error_404_view'
