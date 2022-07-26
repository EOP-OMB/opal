from django.apps import apps
from django.contrib import admin
from common.models import metadata


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
class metadataAdmin(admin.ModelAdmin):
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
    # raw_id_fields = (
    #     'revisions',
    #     'document_ids',
    #     'props',
    #     'links',
    #     'locations',
    #     'parties',
    #     'responsible_parties',
    # )
    date_hierarchy = 'updated_at'


class metadataAdminTabularInline(admin.TabularInline):
    model = metadata


# other models
models = apps.get_app_config('common').get_models()

for model in models:
    try:
        admin.site.register(model, CustomAdmin)
    except admin.sites.AlreadyRegistered:
        pass
