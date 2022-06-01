from django.urls import path

from . import views

urlpatterns = [
    path("", views.metadata, name="sp-idp-metadata"),
    path("acs/", views.acs, name="sp-idp-acs"),
    path("slo/", views.slo, name="sp-idp-slo"),
    path("login/", views.login, name="sp-idp-login"),
    path("test/", views.login, {"test": True}, name="sp-idp-test"),
    path("verify/", views.login, {"verify": True}, name="sp-idp-verify"),
    path("logout/", views.logout, name="sp-idp-logout"),
    path("bootstrap/", views.bootstrap, name="sp_bootstrap" )
]
