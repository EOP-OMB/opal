# Generated by Django 4.1.7 on 2023-02-23 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('component', '0001_squashed_0006_alter_control_implementations_implemented_requirements'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='components',
            options={'ordering': ('title',), 'verbose_name': 'Component', 'verbose_name_plural': 'Components'},
        ),
    ]