import warnings

from django_nine.versions import *  # NOQA

warnings.warn(
    "The `nine` namespace is deprecated, use `django_nine` instead.",
    DeprecationWarning
)
