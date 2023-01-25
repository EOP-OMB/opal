# Generated by Django 4.1.5 on 2023-01-18 18:27

import common.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_squashed_0006_alter_controls_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controls',
            name='sort_id',
            field=common.models.ShortTextField(help_text='normalized value to sort controls in the correct order', null=True, verbose_name='Sort ID'),
        ),
    ]
