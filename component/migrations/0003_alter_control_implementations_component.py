# Generated by Django 4.0.6 on 2022-07-25 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('component', '0002_remove_components_control_implementations_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='control_implementations',
            name='component',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='component.components'),
        ),
    ]