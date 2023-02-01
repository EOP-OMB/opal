# Generated by Django 4.1.5 on 2023-01-17 22:07

import ckeditor.fields
import common.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    replaces = [('ctrl_profile', '0001_initial'), ('ctrl_profile', '0002_imports_tn_ancestors_count_imports_tn_ancestors_pks_and_more'), ('ctrl_profile', '0003_alter_imports_remarks_alter_modify_remarks_and_more'), ('ctrl_profile', '0004_remove_imports_tn_ancestors_count_and_more')]

    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='imports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('href', common.models.ShortTextField(help_text='URI to access the catalog or profiles to be imported', verbose_name='Link to catalog or profiles')),
                ('import_type', common.models.ShortTextField(choices=[('catalog', 'Catalog'), ('profiles', 'Profile')], help_text='Select if this import is for a catalog or a profiles', verbose_name='Type of Import')),
                ('include_all', models.BooleanField(default=True, help_text='Select this option to include all controls from the imported catalog or profiles', verbose_name='Include all controls')),
                ('exclude_controls', common.models.CustomManyToManyField(help_text='Select the controls to be excluded. Any controls not explicitly selected will be excluded', related_name='exclude_controls', to='catalog.controls', verbose_name='Excluded Controls')),
                ('include_controls', common.models.CustomManyToManyField(help_text='Select the controls to be included. Any controls not explicitly selected will be excluded', related_name='include_controls', to='catalog.controls', verbose_name='Included Controls')),
            ],
            options={
                'verbose_name': 'Import',
                'verbose_name_plural': 'Imports',
            },
        ),
        migrations.CreateModel(
            name='modify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('alters', common.models.CustomManyToManyField(help_text='Select any controls you wish to modify', to='catalog.controls', verbose_name='Modified Controls')),
                ('set_parameters', common.models.CustomManyToManyField(help_text='Select any parameters you wish to modify', to='catalog.params', verbose_name='Modified Paramaters')),
            ],
            options={
                'verbose_name': 'Modify Controls',
                'verbose_name_plural': 'Modify Controls',
            },
        ),
        migrations.CreateModel(
            name='profiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('merge', common.models.ShortTextField(choices=[('use-first', 'Use the first definition - the first control with a given ID is used; subsequent ones are discarded'), ('keep', 'Keep - controls with the same ID are kept, retaining the clash')], help_text='A Merge element provides structuring directives that drive how controls are organized after resolution.', null=True, verbose_name='Merge Strategy')),
                ('back_matter', models.ForeignKey(help_text="Provides a collection of identified resource objects that can be referenced by a link with a rel value of 'reference' and an href value that is a fragment '#' followed by a reference to a reference identifier. Other specialized link 'rel' values also use this pattern when indicated in that context of use.", null=True, on_delete=django.db.models.deletion.CASCADE, to='common.back_matter', verbose_name='Back matter')),
                ('imports', common.models.CustomManyToManyField(help_text='The import designates a catalog, profiles, or other resource to be included (referenced and potentially modified) by this profiles. The import also identifies which controls to select using the include-all, include-controls, and exclude-controls directives.', to='ctrl_profile.imports', verbose_name='Imports')),
                ('metadata', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.metadata')),
                ('modify', models.ForeignKey(help_text='Define paramaters and controls that are modified by this profiles.', null=True, on_delete=django.db.models.deletion.CASCADE, to='ctrl_profile.modify', verbose_name='Modifications')),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
    ]