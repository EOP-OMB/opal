# Generated by Django 4.2.5 on 2023-12-08 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0012_alter_back_matter_resources_and_more'),
        ('catalog', '0012_alter_catalogs_controls_alter_catalogs_groups_and_more'),
        ('component', '0014_alter_by_components_links_alter_components_links_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='by_components',
            name='inherited',
            field=models.ManyToManyField(blank=True, help_text='Describes a control implementation inherited by a leveraging system.', to='component.inherited', verbose_name='Inherited Control Implementation'),
        ),
        migrations.AlterField(
            model_name='by_components',
            name='responsible_roles',
            field=models.ManyToManyField(blank=True, help_text='A reference to one or more roles with responsibility for performing a function relative to the containing object.', to='component.responsible_roles', verbose_name='Responsible Roles'),
        ),
        migrations.AlterField(
            model_name='by_components',
            name='satisfied',
            field=models.ManyToManyField(blank=True, help_text='Describes how this system satisfies a responsibility imposed by a leveraged system.', to='component.satisfied', verbose_name='Satisfied Control Implementation Responsibility'),
        ),
        migrations.AlterField(
            model_name='by_components',
            name='set_parameters',
            field=models.ManyToManyField(blank=True, help_text='Identifies the parameter that will be set by the enclosed value. Overrides globally set parameters of the same name', to='component.parameters', verbose_name='Set Parameter Value'),
        ),
        migrations.AlterField(
            model_name='components',
            name='protocols',
            field=models.ManyToManyField(blank=True, help_text='Information about the protocol used to provide a service.', to='common.protocols', verbose_name='Service Protocol Information'),
        ),
        migrations.AlterField(
            model_name='components',
            name='responsible_roles',
            field=models.ManyToManyField(blank=True, help_text='A reference to one or more roles with responsibility for performing a function relative to the containing object.', to='component.responsible_roles', verbose_name='Responsible Roles'),
        ),
        migrations.AlterField(
            model_name='control_implementations',
            name='set_parameters',
            field=models.ManyToManyField(blank=True, help_text='Use of set-parameter in this context, sets the parameter for all related controls referenced in an implemented-requirement. If the same parameter is also set in a specific implemented-requirement, then the new value will override this value.', related_name='set_parameters', to='component.parameters', verbose_name='Common Parameters'),
        ),
        migrations.AlterField(
            model_name='export',
            name='provided',
            field=models.ManyToManyField(blank=True, help_text='Describes a capability which may be inherited by a leveraging system', to='component.provided_control_implementation', verbose_name='Provided Control Implementations'),
        ),
        migrations.AlterField(
            model_name='export',
            name='responsibilities',
            field=models.ManyToManyField(blank=True, help_text='Describes a control implementation responsibility imposed on a leveraging system.', to='component.responsibilities', verbose_name='Control Implementation Responsibility'),
        ),
        migrations.AlterField(
            model_name='implemented_requirements',
            name='responsible_roles',
            field=models.ManyToManyField(blank=True, help_text='A reference to one or more roles with responsibility for performing a function relative to the containing object.', to='component.responsible_roles', verbose_name='Responsible Role'),
        ),
        migrations.AlterField(
            model_name='implemented_requirements',
            name='set_parameters',
            field=models.ManyToManyField(blank=True, help_text='Identifies the parameter that will be set by the enclosed value. Overrides globally set parameters of the same name', to='component.parameters', verbose_name='Set Parameter Value'),
        ),
        migrations.AlterField(
            model_name='inherited',
            name='responsible_roles',
            field=models.ManyToManyField(blank=True, help_text='A reference to one or more roles with responsibility for performing a function relative to the containing object.', to='component.responsible_roles', verbose_name='Responsible Roles'),
        ),
        migrations.AlterField(
            model_name='provided_control_implementation',
            name='responsible_roles',
            field=models.ManyToManyField(blank=True, help_text='A reference to one or more roles with responsibility for performing a function relative to the containing object.', to='component.responsible_roles', verbose_name='Responsible Roles'),
        ),
        migrations.AlterField(
            model_name='responsibilities',
            name='responsible_roles',
            field=models.ManyToManyField(blank=True, help_text='A reference to one or more roles with responsibility for performing a function relative to the containing object.', to='component.responsible_roles', verbose_name='Responsible Roles'),
        ),
        migrations.AlterField(
            model_name='responsible_roles',
            name='party_uuids',
            field=models.ManyToManyField(blank=True, help_text='References a party defined in metadata.', to='common.parties', verbose_name='Party Reference'),
        ),
        migrations.AlterField(
            model_name='satisfied',
            name='responsible_roles',
            field=models.ManyToManyField(blank=True, help_text='A reference to one or more roles with responsibility for performing a function relative to the containing object.', to='component.responsible_roles', verbose_name='Responsible Roles'),
        ),
        migrations.AlterField(
            model_name='statements',
            name='by_components',
            field=models.ManyToManyField(blank=True, help_text='Defines how the referenced component implements a set of controls.', to='component.by_components', verbose_name='Component Control Implementation'),
        ),
        migrations.AlterField(
            model_name='statements',
            name='responsible_roles',
            field=models.ManyToManyField(blank=True, help_text='A reference to one or more roles with responsibility for performing a function relative to the containing object.', to='component.responsible_roles', verbose_name='Responsible Role'),
        ),
        migrations.AlterField(
            model_name='statements',
            name='statement_id',
            field=models.ManyToManyField(blank=True, help_text='A reference to a control statement by its identifier', to='catalog.parts', verbose_name='Control Statement Reference'),
        ),
    ]