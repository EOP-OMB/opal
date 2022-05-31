from __future__ import unicode_literals

from django.contrib import admin

from .models import IdP, IdPAttribute, IdPUserDefaultValue


class IdPAttributeInline(admin.TabularInline):
    model = IdPAttribute
    extra = 0


class IdPUserDefaultValueInline(admin.TabularInline):
    model = IdPUserDefaultValue
    extra = 0


class IdPAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "url_params",
        "last_import",
        "certificate_expires",
        "get_entity_id",
        "is_active",
        "last_login",
    )
    list_filter = ("is_active",)
    actions = ("import_metadata", "generate_certificates")
    inlines = (IdPUserDefaultValueInline, IdPAttributeInline)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "url_params",
                    "base_url",
                    "entity_id",
                    "notes",
                    "is_active",
                )
            },
        ),
        (
            "SP Settings",
            {
                "fields": (
                    "contact_name",
                    "contact_email",
                    "x509_certificate",
                    "private_key",
                    "certificate_expires",
                )
            },
        ),
        (
            "IdP Metadata",
            {
                "fields": (
                    "metadata_url",
                    "verify_metadata_cert",
                    "metadata_xml",
                    "lowercase_encoding",
                    "last_import",
                )
            },
        ),
        (
            "Logins",
            {
                "fields": (
                    "auth_case_sensitive",
                    "create_users",
                    "associate_users",
                    "respect_expiration",
                    "logout_triggers_slo",
                    "login_redirect",
                    "logout_redirect",
                    "last_login",
                )
            },
        ),
        (
            "Advanced",
            {
                "classes": ("collapse",),
                "fields": (
                    "username_prefix",
                    "username_suffix",
                    "state_timeout",
                    "authenticate_method",
                    "login_method",
                    "logout_method",
                ),
            },
        ),
    )
    readonly_fields = ("last_import", "last_login")

    def get_changeform_initial_data(self, request):
        return {
            "base_url": "{}://{}{}".format(
                request.scheme,
                request.get_host(),
                request.META["SCRIPT_NAME"].rstrip("/"),
            )
        }

    def generate_certificates(self, request, queryset):
        for idp in queryset:
            idp.generate_certificate()

    def import_metadata(self, request, queryset):
        for idp in queryset:
            idp.import_metadata()

    def save_model(self, request, obj, form, change):
        super(IdPAdmin, self).save_model(request, obj, form, change)
        try:
            obj.import_metadata()
        except Exception:
            pass


admin.site.register(IdP, IdPAdmin)
