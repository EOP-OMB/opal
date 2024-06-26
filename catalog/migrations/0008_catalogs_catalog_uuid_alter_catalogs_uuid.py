# Generated by Django 4.2 on 2023-06-14 18:42

import common.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_squashed_0007_alter_controls_sort_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalogs',
            name='catalog_uuid',
            field=common.models.ShortTextField(null=True, verbose_name='Catalog Universally Unique Identifier'),
        ),
        migrations.AlterField(
            model_name='catalogs',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
