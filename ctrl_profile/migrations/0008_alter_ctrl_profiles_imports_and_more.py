# Generated by Django 4.2.5 on 2023-12-08 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_alter_catalogs_controls_alter_catalogs_groups_and_more'),
        ('ctrl_profile', '0007_rename_profiles_ctrl_profiles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ctrl_profiles',
            name='imports',
            field=models.ManyToManyField(blank=True, help_text='The import designates a catalog, profiles, or other resource to be included (referenced and potentially modified) by this profiles. The import also identifies which controls to select using the include-all, include-controls, and exclude-controls directives.', to='ctrl_profile.imports', verbose_name='Imports'),
        ),
        migrations.AlterField(
            model_name='imports',
            name='exclude_controls',
            field=models.ManyToManyField(blank=True, help_text='Select the controls to be excluded. Any controls not explicitly selected will be excluded', related_name='exclude_controls', to='catalog.controls', verbose_name='Excluded Controls'),
        ),
        migrations.AlterField(
            model_name='imports',
            name='include_controls',
            field=models.ManyToManyField(blank=True, help_text='Select the controls to be included. Any controls not explicitly selected will be excluded', related_name='include_controls', to='catalog.controls', verbose_name='Included Controls'),
        ),
        migrations.AlterField(
            model_name='modify',
            name='alters',
            field=models.ManyToManyField(blank=True, help_text='Select any controls you wish to modify', to='catalog.controls', verbose_name='Modified Controls'),
        ),
        migrations.AlterField(
            model_name='modify',
            name='set_parameters',
            field=models.ManyToManyField(blank=True, help_text='Select any parameters you wish to modify', to='catalog.params', verbose_name='Modified Parameters'),
        ),
    ]