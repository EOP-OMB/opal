# Generated by Django 4.2.5 on 2023-09-28 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0009_alter_citations_links_alter_metadata_links_and_more'),
        ('ssp', '0010_alter_authorization_boundaries_links_and_more'),
        ('ctrl_profile', '0006_alter_imports_exclude_controls_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='profiles',
            new_name='ctrl_profiles',
        ),
    ]
