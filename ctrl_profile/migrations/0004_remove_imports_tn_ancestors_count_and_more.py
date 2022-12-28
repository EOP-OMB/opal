# Generated by Django 4.1 on 2022-08-31 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ctrl_profile', '0003_alter_imports_remarks_alter_modify_remarks_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imports',
            name='tn_ancestors_count',
        ),
        migrations.RemoveField(
            model_name='imports',
            name='tn_ancestors_pks',
        ),
        migrations.RemoveField(
            model_name='imports',
            name='tn_children_count',
        ),
        migrations.RemoveField(
            model_name='imports',
            name='tn_children_pks',
        ),
        migrations.RemoveField(
            model_name='imports',
            name='tn_depth',
        ),
        migrations.RemoveField(
            model_name='imports',
            name='tn_descendants_count',
        ),
        migrations.RemoveField(
            model_name='imports',
            name='tn_descendants_pks',
        ),
        migrations.RemoveField(
            model_name='imports',
            name='tn_index',
        ),
        migrations.RemoveField(
            model_name='imports',
            name='tn_level',
        ),
        migrations.RemoveField(
            model_name='imports',
            name='tn_order',
        ),
        migrations.RemoveField(
            model_name='imports',
            name='tn_parent',
        ),
        migrations.RemoveField(
            model_name='imports',
            name='tn_priority',
        ),
        migrations.RemoveField(
            model_name='imports',
            name='tn_siblings_count',
        ),
        migrations.RemoveField(
            model_name='imports',
            name='tn_siblings_pks',
        ),
        migrations.RemoveField(
            model_name='modify',
            name='tn_ancestors_count',
        ),
        migrations.RemoveField(
            model_name='modify',
            name='tn_ancestors_pks',
        ),
        migrations.RemoveField(
            model_name='modify',
            name='tn_children_count',
        ),
        migrations.RemoveField(
            model_name='modify',
            name='tn_children_pks',
        ),
        migrations.RemoveField(
            model_name='modify',
            name='tn_depth',
        ),
        migrations.RemoveField(
            model_name='modify',
            name='tn_descendants_count',
        ),
        migrations.RemoveField(
            model_name='modify',
            name='tn_descendants_pks',
        ),
        migrations.RemoveField(
            model_name='modify',
            name='tn_index',
        ),
        migrations.RemoveField(
            model_name='modify',
            name='tn_level',
        ),
        migrations.RemoveField(
            model_name='modify',
            name='tn_order',
        ),
        migrations.RemoveField(
            model_name='modify',
            name='tn_parent',
        ),
        migrations.RemoveField(
            model_name='modify',
            name='tn_priority',
        ),
        migrations.RemoveField(
            model_name='modify',
            name='tn_siblings_count',
        ),
        migrations.RemoveField(
            model_name='modify',
            name='tn_siblings_pks',
        ),
        migrations.RemoveField(
            model_name='profiles',
            name='tn_ancestors_count',
        ),
        migrations.RemoveField(
            model_name='profiles',
            name='tn_ancestors_pks',
        ),
        migrations.RemoveField(
            model_name='profiles',
            name='tn_children_count',
        ),
        migrations.RemoveField(
            model_name='profiles',
            name='tn_children_pks',
        ),
        migrations.RemoveField(
            model_name='profiles',
            name='tn_depth',
        ),
        migrations.RemoveField(
            model_name='profiles',
            name='tn_descendants_count',
        ),
        migrations.RemoveField(
            model_name='profiles',
            name='tn_descendants_pks',
        ),
        migrations.RemoveField(
            model_name='profiles',
            name='tn_index',
        ),
        migrations.RemoveField(
            model_name='profiles',
            name='tn_level',
        ),
        migrations.RemoveField(
            model_name='profiles',
            name='tn_order',
        ),
        migrations.RemoveField(
            model_name='profiles',
            name='tn_parent',
        ),
        migrations.RemoveField(
            model_name='profiles',
            name='tn_priority',
        ),
        migrations.RemoveField(
            model_name='profiles',
            name='tn_siblings_count',
        ),
        migrations.RemoveField(
            model_name='profiles',
            name='tn_siblings_pks',
        ),
    ]