# Generated by Django 4.2 on 2023-06-20 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('component', '0013_alter_by_components_inherited_and_more'),
        ('common', '0008_alter_back_matter_resources_alter_citations_links_and_more'),
        ('ssp', '0001_squashed_0008_alter_system_security_plans_control_implementation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorization_boundaries',
            name='diagrams',
            field=models.ManyToManyField(help_text='A graphic that provides a visual representation the Authorization Boundary, or some aspect of it.', to='ssp.diagrams', verbose_name='Diagram(s)'),
        ),
        migrations.AlterField(
            model_name='authorization_boundaries',
            name='links',
            field=models.ManyToManyField(null=True, to='common.links', verbose_name='Links'),
        ),
        migrations.AlterField(
            model_name='categorizations',
            name='information_type_ids',
            field=models.ManyToManyField(help_text='An identifier qualified by the given identification system used, such as NIST SP 800-60.', to='ssp.information_type_ids', verbose_name='Information Type Systematized Identifier'),
        ),
        migrations.AlterField(
            model_name='data_flows',
            name='diagrams',
            field=models.ManyToManyField(help_text='A graphic that provides a visual representation the Data Flow, or some aspect of it.', to='ssp.diagrams', verbose_name='Diagram(s)'),
        ),
        migrations.AlterField(
            model_name='data_flows',
            name='links',
            field=models.ManyToManyField(null=True, to='common.links', verbose_name='Links'),
        ),
        migrations.AlterField(
            model_name='diagrams',
            name='links',
            field=models.ManyToManyField(null=True, to='common.links', verbose_name='Links'),
        ),
        migrations.AlterField(
            model_name='information_type_impact_level',
            name='links',
            field=models.ManyToManyField(null=True, to='common.links', verbose_name='Links'),
        ),
        migrations.AlterField(
            model_name='information_types',
            name='categorizations',
            field=models.ManyToManyField(help_text='A set of information type identifiers qualified by the given identification system used, such as NIST SP 800-60.', to='ssp.categorizations', verbose_name='Information Type Categorization'),
        ),
        migrations.AlterField(
            model_name='information_types',
            name='links',
            field=models.ManyToManyField(null=True, to='common.links', verbose_name='Links'),
        ),
        migrations.AlterField(
            model_name='inventory_items',
            name='implemented_components',
            field=models.ManyToManyField(help_text='The set of components that are implemented in a given system inventory item.', to='component.components', verbose_name='Implemented Components'),
        ),
        migrations.AlterField(
            model_name='inventory_items',
            name='links',
            field=models.ManyToManyField(null=True, to='common.links', verbose_name='Links'),
        ),
        migrations.AlterField(
            model_name='inventory_items',
            name='responsible_parties',
            field=models.ManyToManyField(help_text='A reference to a set of organizations or persons that have responsibility for performing a referenced role in the context of the containing object.', to='common.responsible_parties', verbose_name='Responsible Parties'),
        ),
        migrations.AlterField(
            model_name='leveraged_authorizations',
            name='links',
            field=models.ManyToManyField(null=True, to='common.links', verbose_name='Links'),
        ),
        migrations.AlterField(
            model_name='network_architectures',
            name='diagrams',
            field=models.ManyToManyField(help_text='A graphic that provides a visual representation the Network Architecture, or some aspect of it.', to='ssp.diagrams', verbose_name='Diagram(s)'),
        ),
        migrations.AlterField(
            model_name='network_architectures',
            name='links',
            field=models.ManyToManyField(null=True, to='common.links', verbose_name='Links'),
        ),
        migrations.AlterField(
            model_name='privileges',
            name='functions_performed',
            field=models.ManyToManyField(help_text='Describes a function performed for a given authorized privilege by this user class.', to='ssp.system_functions', verbose_name='Functions Performed'),
        ),
        migrations.AlterField(
            model_name='system_characteristics',
            name='links',
            field=models.ManyToManyField(null=True, to='common.links', verbose_name='Links'),
        ),
        migrations.AlterField(
            model_name='system_characteristics',
            name='responsible_parties',
            field=models.ManyToManyField(help_text='A reference to a set of organizations or persons that have responsibility for performing a referenced role in the context of the containing object.', to='common.responsible_parties', verbose_name='Responsible Parties'),
        ),
        migrations.AlterField(
            model_name='system_characteristics',
            name='system_ids',
            field=models.ManyToManyField(help_text='One or more unique identifier(s) for the system described by this system security plan.', to='ssp.system_ids', verbose_name='Alternative System Identifier'),
        ),
        migrations.AlterField(
            model_name='system_characteristics',
            name='system_information',
            field=models.ManyToManyField(help_text='Contains details about all information types that are stored, processed, or transmitted by the system, such as privacy information, and those defined in NIST SP 800-60.', to='ssp.systems_information', verbose_name='System Information'),
        ),
        migrations.AlterField(
            model_name='system_implementations',
            name='components',
            field=models.ManyToManyField(help_text='A defined component that can be part of an implemented system. Components may be products, services, application programming interface (APIs), policies, processes, plans, guidance, standards, or other tangible items that enable security and/or privacy.', to='component.components', verbose_name='Components'),
        ),
        migrations.AlterField(
            model_name='system_implementations',
            name='inventory_items',
            field=models.ManyToManyField(help_text='A set of inventory-item entries that represent the managed inventory instances of the system.', to='ssp.inventory_items', verbose_name='Inventory Items'),
        ),
        migrations.AlterField(
            model_name='system_implementations',
            name='leveraged_authorizations',
            field=models.ManyToManyField(help_text='A description of another authorized system from which this system inherits capabilities that satisfy security requirements. Another term for this concept is a common control provider.', to='ssp.leveraged_authorizations', verbose_name='Leveraged Authorizations'),
        ),
        migrations.AlterField(
            model_name='system_implementations',
            name='links',
            field=models.ManyToManyField(null=True, to='common.links', verbose_name='Links'),
        ),
        migrations.AlterField(
            model_name='system_implementations',
            name='users',
            field=models.ManyToManyField(help_text='A type of user that interacts with the system based on an associated role.', to='ssp.users', verbose_name='System Users'),
        ),
        migrations.AlterField(
            model_name='systems_information',
            name='information_types',
            field=models.ManyToManyField(help_text='Contains details about one information type that is stored, processed, or transmitted by the system, such as privacy information, and those defined in NIST SP 800-60.', to='ssp.information_types', verbose_name='Information Type'),
        ),
        migrations.AlterField(
            model_name='systems_information',
            name='links',
            field=models.ManyToManyField(null=True, to='common.links', verbose_name='Links'),
        ),
        migrations.AlterField(
            model_name='users',
            name='authorized_privileges',
            field=models.ManyToManyField(help_text='Identifies a specific system privilege held by the user, along with an associated description and/or rationale for the privilege.', to='ssp.privileges', verbose_name='Privilege'),
        ),
        migrations.AlterField(
            model_name='users',
            name='links',
            field=models.ManyToManyField(null=True, to='common.links', verbose_name='Links'),
        ),
        migrations.AlterField(
            model_name='users',
            name='role_ids',
            field=models.ManyToManyField(help_text='A reference to the roles served by the user.', to='common.roles', verbose_name='User Role(s)'),
        ),
    ]
