from django.contrib import admin
from django.apps import apps
from common.admin import BaseAdmin
from .models import *

# Register your models here.

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


class control_implementations_inline(admin.TabularInline):
    model = components.control_implementations.through
    verbose_name_plural = "Implimented Controls"
    extra = 1


@admin.register(components)
class componentModelAdmin(BaseAdmin):
    inlines = [responsible_roles_inline, protocols_inline, control_implementations_inline]
    fieldsets = (
        ("Metadata", {
            'fields': ("type", "title", "description", "purpose", "status", "remarks")
            }),
        )