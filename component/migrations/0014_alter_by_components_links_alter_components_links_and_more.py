# Generated by Django 4.2.5 on 2023-09-28 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0009_alter_citations_links_alter_metadata_links_and_more'),
        ('component', '0013_alter_by_components_inherited_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='by_components',
            name='links',
            field=models.ManyToManyField(blank=True, to='common.links', verbose_name='Links'),
        ),
        migrations.AlterField(
            model_name='components',
            name='links',
            field=models.ManyToManyField(blank=True, to='common.links', verbose_name='Links'),
        ),
        migrations.AlterField(
            model_name='export',
            name='links',
            field=models.ManyToManyField(blank=True, to='common.links', verbose_name='Links'),
        ),
        migrations.AlterField(
            model_name='implemented_requirements',
            name='links',
            field=models.ManyToManyField(blank=True, to='common.links', verbose_name='Links'),
        ),
        migrations.AlterField(
            model_name='inherited',
            name='links',
            field=models.ManyToManyField(blank=True, to='common.links', verbose_name='Links'),
        ),
        migrations.AlterField(
            model_name='provided_control_implementation',
            name='links',
            field=models.ManyToManyField(blank=True, to='common.links', verbose_name='Links'),
        ),
        migrations.AlterField(
            model_name='responsibilities',
            name='links',
            field=models.ManyToManyField(blank=True, to='common.links', verbose_name='Links'),
        ),
        migrations.AlterField(
            model_name='responsible_roles',
            name='links',
            field=models.ManyToManyField(blank=True, to='common.links', verbose_name='Links'),
        ),
        migrations.AlterField(
            model_name='satisfied',
            name='links',
            field=models.ManyToManyField(blank=True, to='common.links', verbose_name='Links'),
        ),
        migrations.AlterField(
            model_name='statements',
            name='links',
            field=models.ManyToManyField(blank=True, to='common.links', verbose_name='Links'),
        ),
    ]
