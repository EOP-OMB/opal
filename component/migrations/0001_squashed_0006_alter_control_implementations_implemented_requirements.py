# Generated by Django 4.1.5 on 2023-01-17 22:09

import ckeditor.fields
import common.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    replaces = [('component', '0001_initial'), ('component', '0002_by_components_tn_ancestors_count_and_more'), ('component', '0003_alter_by_components_description_and_more'), ('component', '0004_remove_by_components_tn_ancestors_count_and_more'), ('component', '0005_remove_implemented_requirements_control_implementation_and_more'), ('component', '0006_alter_control_implementations_implemented_requirements')]

    initial = True

    dependencies = [
        ('common', '0001_initial'),
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='provided_control_implementation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', models.TextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('description', models.TextField(help_text='An implementation statement that describes the aspects of the control or control statement implementation that can be provided to another system leveraging this system.', verbose_name='Provided Control Implementation Description')),
                ('links', common.models.CustomManyToManyField(to='common.links', verbose_name='Links')),
                ('props', common.models.properties_field(to='common.props')),
            ],
            options={
                'verbose_name': 'Provided Control Implementation',
                'verbose_name_plural': 'Provided Control Implementations',
            },
        ),
        migrations.CreateModel(
            name='responsibilities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', models.TextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('description', models.TextField(help_text='An implementation statement that describes the aspects of the control or control statement implementation that a leveraging system must implement to satisfy the control provided by a leveraged system.', verbose_name='Control Implementation Responsibility Description')),
                ('links', common.models.CustomManyToManyField(to='common.links', verbose_name='Links')),
                ('props', common.models.properties_field(to='common.props')),
                ('provided_uuid', models.ForeignKey(blank=True, help_text=" Identifies a 'provided' assembly associated with this assembly.", on_delete=django.db.models.deletion.CASCADE, to='component.provided_control_implementation', verbose_name='Provided Control Implementation')),
            ],
            options={
                'verbose_name': 'Control Implementation Responsibility',
                'verbose_name_plural': 'Control Implementation Responsibilities',
            },
        ),
        migrations.CreateModel(
            name='responsible_roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('links', common.models.CustomManyToManyField(to='common.links', verbose_name='Links')),
                ('party_uuids', common.models.CustomManyToManyField(help_text='References a party defined in metadata.', to='common.parties', verbose_name='Party Reference')),
                ('props', common.models.properties_field(to='common.props')),
                ('role_id', models.ForeignKey(help_text='The role that is responsible for the business function.', on_delete=django.db.models.deletion.CASCADE, to='common.roles', verbose_name='Role')),
            ],
            options={
                'verbose_name': 'Responsible Role',
                'verbose_name_plural': 'Responsible Roles',
            },
        ),
        migrations.CreateModel(
            name='satisfied',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('description', ckeditor.fields.RichTextField(help_text='An implementation statement that describes the aspects of a control or control statement implementation that a leveraging system is inheriting from a leveraged system.', verbose_name='Control Implementation Responsibility Description')),
                ('links', common.models.CustomManyToManyField(to='common.links', verbose_name='Links')),
                ('props', common.models.properties_field(to='common.props')),
                ('responsibility_uuid', models.ForeignKey(blank=True, help_text=" Identifies a 'provided' assembly associated with this assembly.", on_delete=django.db.models.deletion.CASCADE, to='component.responsibilities', verbose_name='Provided Control Implementation')),
                ('responsible_roles', common.models.CustomManyToManyField(help_text='A reference to one or more roles with responsibility for performing a function relative to the containing object.', to='component.responsible_roles', verbose_name='Responsible Roles')),
            ],
            options={
                'verbose_name': 'Satisfied Control Implementation Responsibility',
                'verbose_name_plural': 'Satisfied Control Implementation Responsibilities',
            },
        ),
        migrations.AddField(
            model_name='responsibilities',
            name='responsible_roles',
            field=common.models.CustomManyToManyField(help_text='A reference to one or more roles with responsibility for performing a function relative to the containing object.', to='component.responsible_roles', verbose_name='Responsible Roles'),
        ),
        migrations.AddField(
            model_name='provided_control_implementation',
            name='responsible_roles',
            field=common.models.CustomManyToManyField(help_text='A reference to one or more roles with responsibility for performing a function relative to the containing object.', to='component.responsible_roles', verbose_name='Responsible Roles'),
        ),
        migrations.CreateModel(
            name='parameters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', models.TextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('values', common.models.ShortTextField(help_text='A parameter value or set of values.', verbose_name='Parameter Value')),
                ('param_id', models.ForeignKey(help_text="A reference to a parameter within a control, who's catalog has been imported into the current implementation context.", on_delete=django.db.models.deletion.CASCADE, to='catalog.params', verbose_name='Parameter')),
            ],
            options={
                'verbose_name': 'Parameter',
                'verbose_name_plural': 'Parameters',
            },
        ),
        migrations.CreateModel(
            name='inherited',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('description', ckeditor.fields.RichTextField(help_text='An implementation statement that describes the aspects of a control or control statement implementation that a leveraging system is inheriting from a leveraged system.', verbose_name='Control Implementation Responsibility Description')),
                ('links', common.models.CustomManyToManyField(to='common.links', verbose_name='Links')),
                ('props', common.models.properties_field(to='common.props')),
                ('provided_uuid', models.ForeignKey(blank=True, help_text=" Identifies a 'provided' assembly associated with this assembly.", on_delete=django.db.models.deletion.CASCADE, to='component.provided_control_implementation', verbose_name='Provided Control Implementation')),
                ('responsible_roles', common.models.CustomManyToManyField(help_text='A reference to one or more roles with responsibility for performing a function relative to the containing object.', to='component.responsible_roles', verbose_name='Responsible Roles')),
            ],
            options={
                'verbose_name': 'Inherited Control Implementation',
                'verbose_name_plural': 'Inherited Control Implementations',
            },
        ),
        migrations.CreateModel(
            name='implemented_requirements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('control_id', models.ForeignKey(help_text='A reference to a control with a corresponding id value.', on_delete=django.db.models.deletion.CASCADE, to='catalog.controls', verbose_name='Control Identifier Reference')),
                ('links', common.models.CustomManyToManyField(to='common.links', verbose_name='Links')),
                ('props', common.models.properties_field(to='common.props')),
                ('responsible_roles', common.models.CustomManyToManyField(help_text='A reference to one or more roles with responsibility for performing a function relative to the containing object.', to='component.responsible_roles', verbose_name='Responsible Role')),
                ('set_parameters', common.models.CustomManyToManyField(help_text='Identifies the parameter that will be set by the enclosed value. Overrides globally set parameters of the same name', to='component.parameters', verbose_name='Set Parameter Value')),
            ],
            options={
                'verbose_name': 'Implemented Requirement',
                'verbose_name_plural': 'Implemented Requirements',
            },
        ),
        migrations.CreateModel(
            name='export',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('description', ckeditor.fields.RichTextField(help_text='An implementation statement that describes the aspects of the control or control statement implementation that can be available to another system leveraging this system.', verbose_name='Control Implementation Export Description')),
                ('links', common.models.CustomManyToManyField(to='common.links', verbose_name='Links')),
                ('props', common.models.properties_field(to='common.props')),
                ('provided', common.models.CustomManyToManyField(help_text='Describes a capability which may be inherited by a leveraging system', to='component.provided_control_implementation', verbose_name='Provided Control Implementations')),
                ('responsibilities', common.models.CustomManyToManyField(help_text='Describes a control implementation responsibility imposed on a leveraging system.', to='component.responsibilities', verbose_name='Control Implementation Responsibility')),
            ],
            options={
                'verbose_name': 'Export',
                'verbose_name_plural': 'Exports',
            },
        ),
        migrations.CreateModel(
            name='components',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('type', common.models.ShortTextField(choices=[('this-system', 'This System: The system as a whole.'), ('system', 'Another System: An external system, which may be a leveraged system or the other side of an interconnection.'), ('interconnection', 'System Interconnection: A connection to something outside this system.'), ('software', 'Software: Any software, operating system, or firmware.'), ('hardware', 'Hardware: A physical device.'), ('service', 'Service: A service that may provide APIs.'), ('policy', 'Policy: An enforceable policy.'), ('physical', 'Physical: A tangible asset used to provide physical protections or countermeasures.'), ('process-procedure', 'Process or Procedure: A list of steps or actions to take to achieve some end result.'), ('plan', 'Plan: An applicable plan.'), ('guidance', 'Guidance: Any guideline or recommendation.'), ('standard', 'Standard: Any organizational or industry standard.'), ('validation', 'Validation: An external assessment performed on some other component, that has been validated by a third-party.'), ('network', 'Network: A physical or virtual network.')], help_text='A category describing the purpose of the component.', verbose_name='Component Type')),
                ('title', common.models.ShortTextField(help_text='A human readable name for the system component.', verbose_name='Component Title')),
                ('description', ckeditor.fields.RichTextField(help_text='A description of the component, including information about its function.', verbose_name='Component Description')),
                ('purpose', common.models.ShortTextField(help_text='A summary of the technological or business purpose of the component.', verbose_name='Purpose')),
                ('status', common.models.ShortTextField(choices=[('operational', 'Operational: The system or component is currently operating in production.'), ('under-development', 'Under Development: The system or component is being designed, developed, or implemented'), ('under-major-modification', 'Under Major Modification: The system or component is undergoing a major change, development, or transition.'), ('disposition', 'Disposition: The system or component is no longer operational.'), ('other', 'Other: Some other state, a remark must be included to describe the current state.')], help_text=' Describes the operational status of the system component.', verbose_name='Status')),
                ('links', common.models.CustomManyToManyField(to='common.links', verbose_name='Links')),
                ('props', common.models.properties_field(to='common.props')),
                ('protocols', common.models.CustomManyToManyField(help_text='Information about the protocol used to provide a service.', to='common.protocols', verbose_name='Service Protocol Information')),
                ('responsible_roles', common.models.CustomManyToManyField(help_text='A reference to one or more roles with responsibility for performing a function relative to the containing object.', to='component.responsible_roles', verbose_name='Responsible Roles')),
            ],
            options={
                'verbose_name': 'Component',
                'verbose_name_plural': 'Components',
            },
        ),
        migrations.CreateModel(
            name='by_components',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('description', ckeditor.fields.RichTextField(help_text='An implementation statement that describes how a control or a control statement is implemented within the referenced system component.', verbose_name='Control Implementation Description')),
                ('implementation_status', common.models.ShortTextField(choices=[('implemented', 'Implemented: The control is fully implemented.'), ('partial', 'Partial: The control is partially implemented.'), ('planned', 'Planned: There is a plan for implementing the control as explained in the remarks.'), ('alternative', 'Alternative: There is an alternative implementation for this control as explained in the remarks.'), ('not-applicable', 'Not-Applicable: This control does not apply to this system as justified in the remarks.')], help_text='Indicates the degree to which the a given control is implemented.', verbose_name='Implementation Status')),
                ('component_uuid', models.ForeignKey(help_text='A reference to the component that is implementing a given control or control statement.', on_delete=django.db.models.deletion.CASCADE, to='component.components', verbose_name='Component Universally Unique Identifier Reference')),
                ('export', models.ForeignKey(help_text='Identifies content intended for external consumption, such as with leveraged organizations.', null=True, on_delete=django.db.models.deletion.CASCADE, to='component.export', verbose_name='Export')),
                ('inherited', common.models.CustomManyToManyField(help_text='Describes a control implementation inherited by a leveraging system.', to='component.inherited', verbose_name='Inherited Control Implementation')),
                ('links', common.models.CustomManyToManyField(to='common.links', verbose_name='Links')),
                ('props', common.models.properties_field(to='common.props')),
                ('responsible_roles', common.models.CustomManyToManyField(help_text='A reference to one or more roles with responsibility for performing a function relative to the containing object.', to='component.responsible_roles', verbose_name='Responsible Roles')),
                ('satisfied', common.models.CustomManyToManyField(help_text='Describes how this system satisfies a responsibility imposed by a leveraged system.', to='component.satisfied', verbose_name='Satisfied Control Implementation Responsibility')),
                ('set_parameters', common.models.CustomManyToManyField(help_text='Identifies the parameter that will be set by the enclosed value. Overrides globally set parameters of the same name', to='component.parameters', verbose_name='Set Parameter Value')),
                ('implemented_requirement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='component.implemented_requirements')),
            ],
            options={
                'verbose_name': 'Component Control Implementation',
                'verbose_name_plural': 'Component Control Implementations',
            },
        ),
        migrations.AddField(
            model_name='parameters',
            name='by_component',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='component.by_components'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='parameters',
            name='remarks',
            field=ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks'),
        ),
        migrations.AlterField(
            model_name='provided_control_implementation',
            name='description',
            field=ckeditor.fields.RichTextField(help_text='An implementation statement that describes the aspects of the control or control statement implementation that can be provided to another system leveraging this system.', verbose_name='Provided Control Implementation Description'),
        ),
        migrations.AlterField(
            model_name='provided_control_implementation',
            name='remarks',
            field=ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks'),
        ),
        migrations.AlterField(
            model_name='responsibilities',
            name='description',
            field=ckeditor.fields.RichTextField(help_text='An implementation statement that describes the aspects of the control or control statement implementation that a leveraging system must implement to satisfy the control provided by a leveraged system.', verbose_name='Control Implementation Responsibility Description'),
        ),
        migrations.AlterField(
            model_name='responsibilities',
            name='remarks',
            field=ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks'),
        ),
        migrations.CreateModel(
            name='statements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('by_components', common.models.CustomManyToManyField(help_text='Defines how the referenced component implements a set of controls.', to='component.by_components', verbose_name='Component Control Implementation')),
                ('links', common.models.CustomManyToManyField(to='common.links', verbose_name='Links')),
                ('props', common.models.properties_field(to='common.props')),
                ('responsible_roles', common.models.CustomManyToManyField(help_text='A reference to one or more roles with responsibility for performing a function relative to the containing object.', to='component.responsible_roles', verbose_name='Responsible Role')),
                ('statement_id', common.models.CustomManyToManyField(help_text='A reference to a control statement by its identifier', to='catalog.parts', verbose_name='Control Statement Reference')),
                ('implemented_requirement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='component.implemented_requirements')),
            ],
            options={
                'verbose_name': 'Statement',
                'verbose_name_plural': 'Statements',
            },
        ),
        migrations.CreateModel(
            name='control_implementations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('description', ckeditor.fields.RichTextField(help_text='Describes how the system satisfies a set of controls.', verbose_name='Description')),
                ('set_parameters', common.models.CustomManyToManyField(help_text='Use of set-parameter in this context, sets the parameter for all related controls referenced in an implemented-requirement. If the same parameter is also set in a specific implemented-requirement, then the new value will override this value.', to='component.parameters', verbose_name='Common Parameters')),
                ('component', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='component.components')),
                ('implemented_requirements', common.models.CustomManyToManyField(help_text='Set of controls implemented by this component', to='component.implemented_requirements', verbose_name='Implemented Requirements')),
            ],
            options={
                'verbose_name': 'Control Implementation',
                'verbose_name_plural': 'Control Implementations',
            },
        ),
    ]
