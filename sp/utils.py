import datetime

from django.conf import settings
from django.contrib import auth
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import get_object_or_404
from django.utils.module_loading import import_string

from .models import IdP

IDP_SESSION_KEY = "_idpid"
NAMEID_SESSION_KEY = "_nameid"


def authenticate(request, idp, saml):
    return auth.authenticate(request, idp=idp, saml=saml)


def login(request, user, idp, saml):
    auth.login(request, user)
    # Store the authenticating IdP and actual (not mapped) SAML nameid in the session.
    set_session_idp(request, idp, saml.get_nameid())
    if idp.respect_expiration:
        if not settings.SESSION_SERIALIZER.endswith("PickleSerializer"):
            raise ImproperlyConfigured(
                "IdP-based session expiration is only supported with the "
                "PickleSerializer SESSION_SERIALIZER."
            )
        try:
            dt = datetime.datetime.fromtimestamp(
                saml.get_session_expiration(), tz=datetime.timezone.utc
            )
            request.session.set_expiry(dt)
        except TypeError:
            pass


def logout(request, idp):
    auth.logout(request)
    clear_session_idp(request)


def get_request_idp(request, **kwargs):
    custom_loader = getattr(settings, "SP_IDP_LOADER", None)
    if custom_loader:
        return import_string(custom_loader)(request, **kwargs)
    else:
        if IdP.objects.count == 0:
            return "No IDP is defined"
        elif IdP.objects.filter(url_params=kwargs, is_active=True).exists():
            idp =  IdP.objects.get(url_params=kwargs, is_active=True)
        else:
            idp = IdP.objects.first()
        return idp


def get_session_idp(request):
    return IdP.objects.filter(pk=request.session.get(IDP_SESSION_KEY)).first()


def get_session_nameid(request):
    return request.session.get(NAMEID_SESSION_KEY)


def set_session_idp(request, idp, nameid):
    request.session[IDP_SESSION_KEY] = idp.pk
    request.session[NAMEID_SESSION_KEY] = nameid


def clear_session_idp(request):
    for key in (IDP_SESSION_KEY, NAMEID_SESSION_KEY):
        try:
            del request.session[key]
        except KeyError:
            pass
