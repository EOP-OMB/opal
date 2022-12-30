# Generated by Django 4.1.3 on 2022-12-28 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_remove_available_catalog_list_tn_ancestors_count_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='controls',
            options={'verbose_name': 'Control', 'verbose_name_plural': 'Controls'},
        ),
        migrations.AddField(
            model_name='controls',
            name='sort_id',
            field=models.TextField(help_text='normalized value to sort controls in the correct order', max_length=25, null=True, verbose_name='Sort ID'),
        ),
    ]