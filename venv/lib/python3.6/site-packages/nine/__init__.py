import warnings

from django_nine import versions  # NOQA
from django_nine import context_processors  # NOQA

warnings.warn(
    "The `nine` namespace is deprecated, use `django_nine` instead.",
    DeprecationWarning
)
