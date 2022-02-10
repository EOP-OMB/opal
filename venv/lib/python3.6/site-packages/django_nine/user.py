"""
Compatibility module for safe and sane User model import.
"""

import importlib
import warnings

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .versions import DJANGO_LTE_1_4, DJANGO_LTE_1_6, DJANGO_GTE_1_7

if DJANGO_LTE_1_4:
    from django.contrib.auth.models import User
else:
    # Cannot use contrib.auth.get_user_model() at compile time.
    user_app_name, user_model_name = settings.AUTH_USER_MODEL.rsplit('.', 1)
    User = None

    if DJANGO_LTE_1_6:
        for app in settings.INSTALLED_APPS:
            if app.endswith(user_app_name):
                user_app_models = importlib.import_module(app + ".models")
                User = getattr(user_app_models, user_model_name)
                break
    elif DJANGO_GTE_1_7:
        from django.apps import apps
        try:
            User = apps.get_registered_model(user_app_name, user_model_name)
        except KeyError:
            pass

    if User is None:
        raise ImproperlyConfigured(
            "You have defined a custom user model {0}, but the app {1} is "
            "not in ``settings.INSTALLED_APPS``"
            "".format(settings.AUTH_USER_MODEL, user_app_name)
        )

__title__ = 'nine.user'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2015-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('User',)


warnings.warn(
    "The `django_nine.user` module is deprecated and will be removed in "
    "version 0.3.",
    DeprecationWarning
)
