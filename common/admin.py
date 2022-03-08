from django.contrib import admin

# Register your models here.

from .models import port_ranges, protocols, props, links, revisions, document_ids, roles, emails, telephone_numbers, addresses, locations, external_ids, organizations, parties, responsible_parties, metadata, citations, hashes, rlinks, base64, resources, back_matter


@admin.register(port_ranges)
class port_rangesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'start',
        'end',
        'transport',
    )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(protocols)
class protocolsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'name',
        'title',
    )
    list_filter = ('created_at', 'updated_at')
    raw_id_fields = ('port_ranges',)
    search_fields = ('name',)
    date_hierarchy = 'created_at'


@admin.register(props)
class propsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'name',
        'ns',
        'value',
        'property_class',
    )
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name',)
    date_hierarchy = 'created_at'


@admin.register(links)
class linksAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'href',
        'rel',
        'media_type',
        'text',
    )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(revisions)
class revisionsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'title',
        'published',
        'last_modified',
        'version',
        'oscal_version',
    )
    list_filter = ('created_at', 'updated_at', 'published', 'last_modified')
    raw_id_fields = ('props',)
    date_hierarchy = 'created_at'


@admin.register(document_ids)
class document_idsAdmin(admin.ModelAdmin):
    list_display = ('id', 'scheme', 'identifier')


@admin.register(roles)
class rolesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'role_id',
        'title',
        'short_name',
        'description',
    )
    list_filter = ('created_at', 'updated_at')
    raw_id_fields = ('props', 'links')
    date_hierarchy = 'created_at'


@admin.register(emails)
class emailsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'email_address',
    )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(telephone_numbers)
class telephone_numbersAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'type',
        'number',
    )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(addresses)
class addressesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'type',
        'addr_lines',
        'city',
        'state',
        'postal_code',
        'country',
    )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(locations)
class locationsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'title',
        'address',
    )
    list_filter = ('created_at', 'updated_at', 'address')
    raw_id_fields = (
        'email_addresses',
        'telephone_numbers',
        'urls',
        'props',
        'links',
    )
    date_hierarchy = 'created_at'


@admin.register(external_ids)
class external_idsAdmin(admin.ModelAdmin):
    list_display = ('id', 'scheme', 'external_id')


@admin.register(organizations)
class organizationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'created_at', 'updated_at', 'remarks')
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(parties)
class partiesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'type',
        'name',
        'short_name',
        'address',
    )
    list_filter = ('created_at', 'updated_at', 'address')
    raw_id_fields = (
        'external_ids',
        'props',
        'links',
        'email_addresses',
        'telephone_numbers',
        'location_uuids',
        'member_of_organizations',
    )
    search_fields = ('name',)
    date_hierarchy = 'created_at'


@admin.register(responsible_parties)
class responsible_partiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'created_at', 'updated_at', 'role_id')
    list_filter = ('created_at', 'updated_at')
    raw_id_fields = ('party_uuids', 'props', 'links')
    date_hierarchy = 'created_at'


@admin.register(metadata)
class metadataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'title',
        'published',
        'last_modified',
        'version',
        'oscal_version',
    )
    list_filter = ('created_at', 'updated_at', 'published', 'last_modified')
    raw_id_fields = (
        'revisions',
        'document_ids',
        'props',
        'links',
        'locations',
        'parties',
        'responsible_parties',
    )
    date_hierarchy = 'created_at'


@admin.register(citations)
class citationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'created_at', 'updated_at', 'text')
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(hashes)
class hashesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'algorithm',
        'value',
    )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(rlinks)
class rlinksAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(base64)
class base64Admin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'filename',
        'media_type',
        'value',
    )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(resources)
class resourcesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'title',
        'description',
    )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(back_matter)
class back_matterAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    raw_id_fields = ('resources',)
    date_hierarchy = 'created_at'