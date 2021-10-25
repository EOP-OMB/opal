# Generated by Django 3.1.8 on 2021-10-19 18:29

from django.db import migrations
import ssp.models.base_classes_and_fields


class Migration(migrations.Migration):

    dependencies = [
        ('ssp', '0003_test_evidence'),
    ]

    operations = [
        migrations.AddField(
            model_name='test_evidence',
            name='controls',
            field=ssp.models.base_classes_and_fields.customMany2ManyField(blank=True, to='ssp.system_control'),
        ),
    ]