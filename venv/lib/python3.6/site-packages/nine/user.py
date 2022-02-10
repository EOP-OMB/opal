import warnings

from django_nine.user import *  # NOQA


warnings.warn(
    "The `nine` namespace is deprecated, use `django_nine` instead.",
    DeprecationWarning
)

warnings.warn(
    "The `django_nine.user` module is deprecated and will be removed in "
    "version 0.3.",
    DeprecationWarning
)
