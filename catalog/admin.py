from django.contrib import admin

# Register your models here.
from .models import tests, constraints, guidelines, params, parts, controls, groups, catalogs

@admin.register(tests)
class testsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'expression',
    )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(constraints)
class constraintsAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'created_at', 'updated_at', 'description')
    list_filter = ('created_at', 'updated_at')
    raw_id_fields = ('tests',)
    date_hierarchy = 'created_at'


@admin.register(guidelines)
class guidelinesAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'created_at', 'updated_at', 'prose')
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(params)
class paramsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'remarks',
        'param_id',
        'param_class',
        'depends_on',
        'label',
        'usage',
        'values',
        'select',
        'how_many',
        'choice',
    )
    list_filter = ('created_at', 'updated_at')
    raw_id_fields = ('depends_on',)
    date_hierarchy = 'created_at'


@admin.register(parts)
class partsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'part_id',
        'name',
        'ns',
        'part_class',
        'title',
        'prose',
    )
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name',)
    date_hierarchy = 'created_at'


@admin.register(controls)
class controlsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'control_id',
        'control_class',
        'title',
    )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(groups)
class groupsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'created_at',
        'updated_at',
        'group_id',
        'group_class',
        'title',
    )
    list_filter = ('created_at', 'updated_at')
    raw_id_fields = (
        'params',
        'props',
        'links',
        'parts',
        'sub_groups',
        'controls',
    )
    date_hierarchy = 'created_at'


@admin.register(catalogs)
class catalogsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'updated_at',
        'uuid',
        'metadata',
        'back_matter',
    )
    list_filter = ('created_at', 'updated_at', 'metadata', 'back_matter')
    raw_id_fields = ('params', 'controls', 'groups')
    date_hierarchy = 'created_at'