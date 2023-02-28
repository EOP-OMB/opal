# Generated by Django 4.1.7 on 2023-02-23 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('component', '0007_alter_components_options'),
        ('ssp', '0007_alter_import_profiles_href'),
    ]

    operations = [
        migrations.AlterField(
            model_name='system_security_plans',
            name='control_implementation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='component.control_implementations'),
        ),
    ]