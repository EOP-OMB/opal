# Generated by Django 4.0.6 on 2022-07-13 21:17

from django.db import migrations, models
import uuid
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='available_catalog_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', models.TextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('slug', common.models.ShortTextField(help_text='A short name used to identify the catalog in functions or queries. Lowercase, no spaces.', verbose_name='Catalog Slug')),
                ('link', models.URLField(help_text='A complete URL which returns valid OSCAL json text', verbose_name='Link to Catalog')),
                ('name', common.models.ShortTextField(help_text='Human readable name of the catalog.', verbose_name='Catalog Title')),
                ],
            options={
                'verbose_name': 'Catalog Source',
                'verbose_name_plural': 'Catalog Sources',
                },
            ),
        migrations.AddField(
            model_name='available_catalog_list',
            name='catalog_uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.AlterField(
            model_name='available_catalog_list',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
