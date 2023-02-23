from django.apps import apps
from django.contrib import admin
from common.models import metadata, port_ranges, protocols, props, links, revisions, document_ids, roles, emails, telephone_numbers, addresses, locations, external_ids, organizations, parties, responsible_parties, metadata, citations, hashes, rlinks, base64, \
    resources, back_matter


# Register your models here.

class CustomAdmin(admin.ModelAdmin):

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        """
        Get a form Field for a ManyToManyField. Tweak so filter_horizontal
        control used by default. If raw_id or autocomplete are specified
        will take precedence over this.
        """
        filter_horizontal_original = self.filter_horizontal
        self.filter_horizontal = (db_field.name,)
        form_field = super().formfield_for_manytomany(db_field, request=None, **kwargs)
        self.filter_horizontal = filter_horizontal_original
        return form_field

    def get_list_display(self, request):
        """
        Return a sequence containing the fields to be displayed on the
        changelist.
        """
        excluded_fields = ['created_at', 'updated_at']
        self.list_display = []
        for field in self.opts.concrete_fields:
            print("field = " + field.name)
            if field.name not in excluded_fields:
                self.list_display.append(field.name)
        self.list_display.append('created_at')
        self.list_display.append('updated_at')
        print(self.list_display)
        return self.list_display


@admin.register(metadata)
class metadataAdmin(CustomAdmin):
    list_display = (
        'title',
        'published',
        'last_modified',
        'version',
        'oscal_version',
        'created_at',
        'updated_at'
        )
    list_filter = ('created_at', 'updated_at', 'published', 'last_modified')
    date_hierarchy = 'updated_at'
    fieldsets = (
     (None, {'fields': ['title','published','last_modified','version']}),
     ('Advanced', {'classes': ('collapse',),'fields': ['oscal_version','revisions','document_ids','props','links','locations','parties','responsible_parties']}),
    )


class metadataAdminTabularInline(admin.TabularInline):
    model = metadata


@admin.register(port_ranges)
class port_rangesAdmin(CustomAdmin):
    list_display = (
        'start',
        'end',
        'transport',
        'created_at',
        'updated_at',
        )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'updated_at'


@admin.register(protocols)
class protocolsAdmin(CustomAdmin):
    list_display = (
        'name',
        'title',
        'created_at',
        'updated_at',
        )
    list_filter = ('created_at', 'updated_at')
    raw_id_fields = ('port_ranges',)
    search_fields = ('name',)
    date_hierarchy = 'updated_at'


@admin.register(props)
class propsAdmin(CustomAdmin):
    list_display = (
        'name',
        'ns',
        'value',
        'property_class',
        'created_at',
        'updated_at',
        )
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name',)
    date_hierarchy = 'updated_at'


@admin.register(links)
class linksAdmin(CustomAdmin):
    list_display = (
        'href',
        'rel',
        'media_type',
        'text',
        'created_at',
        'updated_at',
        )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'updated_at'


@admin.register(revisions)
class revisionsAdmin(CustomAdmin):
    list_display = (
        'title',
        'published',
        'last_modified',
        'version',
        'oscal_version',
        'created_at',
        'updated_at',
        'remarks',
        )
    list_filter = (
        'created_at',
        'updated_at',
        'published',
        'last_modified',
        )
    raw_id_fields = ('props',)
    date_hierarchy = 'updated_at'


@admin.register(document_ids)
class document_idsAdmin(CustomAdmin):
    list_display = (
        'scheme',
        'identifier',
        'created_at',
        'updated_at',
        )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'updated_at'


@admin.register(roles)
class rolesAdmin(CustomAdmin):
    list_display = (
        'role_id',
        'title',
        'short_name',
        'description',
        'created_at',
        'updated_at',
        )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'updated_at'


@admin.register(emails)
class emailsAdmin(CustomAdmin):
    list_display = (
        'email_address',
        'created_at',
        'updated_at',
        'remarks',
        )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'updated_at'


@admin.register(telephone_numbers)
class telephone_numbersAdmin(CustomAdmin):
    list_display = (
        'type',
        'number',
        'created_at',
        'updated_at',
        'remarks',
        )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'updated_at'


@admin.register(addresses)
class addressesAdmin(CustomAdmin):
    list_display = (
        'type',
        'addr_lines',
        'city',
        'state',
        'postal_code',
        'country',
        'created_at',
        'updated_at',
        )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'updated_at'


@admin.register(locations)
class locationsAdmin(CustomAdmin):
    list_display = (
        'title',
        'address',
        'created_at',
        'updated_at',
        )
    list_filter = ('created_at', 'updated_at', 'address')
    date_hierarchy = 'updated_at'


@admin.register(external_ids)
class external_idsAdmin(CustomAdmin):
    list_display = ('id', 'scheme', 'external_id')


@admin.register(organizations)
class organizationsAdmin(CustomAdmin):
    list_display = (
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'updated_at'


@admin.register(parties)
class partiesAdmin(CustomAdmin):
    list_display = (
        'type',
        'name',
        'short_name',
        'address',
        'created_at',
        'updated_at',
        'remarks',
        )
    list_filter = ('created_at', 'updated_at', 'address')
    search_fields = ('name',)
    date_hierarchy = 'updated_at'


@admin.register(responsible_parties)
class responsible_partiesAdmin(CustomAdmin):
    list_display = (
        'role_id',
        'uuid',
        'created_at',
        'updated_at',
        )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'updated_at'


@admin.register(citations)
class citationsAdmin(CustomAdmin):
    list_display = (
        'text',
        'created_at',
        'updated_at',
        )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'updated_at'


@admin.register(hashes)
class hashesAdmin(CustomAdmin):
    list_display = (
        'value',
        'algorithm',
        'created_at',
        'updated_at',
        )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'updated_at'


@admin.register(rlinks)
class rlinksAdmin(CustomAdmin):
    list_display = (
        'uuid',
        'created_at',
        'updated_at',
        )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'updated_at'


@admin.register(base64)
class base64Admin(CustomAdmin):
    list_display = (
        'uuid',
        'filename',
        'media_type',
        'value',
        'created_at',
        'updated_at',
        )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'updated_at'


@admin.register(resources)
class resourcesAdmin(CustomAdmin):
    list_display = (
        'title',
        'description',
        'created_at',
        'updated_at',
        )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'updated_at'


@admin.register(back_matter)
class back_matterAdmin(CustomAdmin):
    list_display = (
        'uuid',
        'created_at',
        'updated_at',
        )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'updated_at'


# other models
# models = apps.get_app_config('common').get_models()
#
# for model in models:
#     try:
#         admin.site.register(model, CustomAdmin)
#     except admin.sites.AlreadyRegistered:
#         pass
