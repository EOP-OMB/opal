# Generated by Django 4.1 on 2022-08-30 16:43

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_available_catalog_list_tn_ancestors_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='available_catalog_list',
            name='remarks',
            field=ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks'),
        ),
        migrations.AlterField(
            model_name='params',
            name='remarks',
            field=ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks'),
        ),
        migrations.AlterField(
            model_name='tests',
            name='remarks',
            field=ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks'),
        ),
    ]
