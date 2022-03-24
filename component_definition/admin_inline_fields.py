from django.contrib import admin
from .models import *


class implemented_requirements_inline(admin.TabularInline):
    model = control_implementations.implemented_requirements.through
    verbose_name_plural = "Implemented Requirements"
    extra = 1


class control_implementations_inline(admin.TabularInline):
    model = components.control_implementations.through
    verbose_name_plural = "Implemented Controls"
    extra = 1


class responsible_roles_inline(admin.TabularInline):
    model = components.responsible_roles.through
    verbose_name_plural = "Responsible Roles (if required)"
    verbose_name = "Role"
    extra = 1


class protocols_inline(admin.TabularInline):
    model = components.protocols.through
    verbose_name_plural = "Protocols (if required)"
    verbose_name = "Protocol"
    extra = 1
