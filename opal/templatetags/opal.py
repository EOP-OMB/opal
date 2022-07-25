from django import template
from opal import __build__

register = template.Library()


@register.filter
def version():
    return __build__()
