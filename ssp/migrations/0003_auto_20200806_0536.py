# Generated by Django 3.1 on 2020-08-06 10:36

from django.db import migrations, models
import ssp.models


class Migration(migrations.Migration):

    dependencies = [
        ('ssp', '0002_auto_20200805_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='system_characteristic',
            name='security_impact_level',
            field=models.CharField(blank=True, choices=[('high', 'High'), ('moderate', 'Moderate'), ('low', 'Low')], max_length=30),
        ),
        migrations.AddField(
            model_name='system_characteristic',
            name='system_information',
            field=ssp.models.customMany2ManyField(blank=True, to='ssp.system_information_type'),
        ),
    ]
