# Generated by Django 3.1.8 on 2021-11-05 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ssp', '0006_auto_20211028_1410'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test_evidence',
            name='results',
        ),
        migrations.AddField(
            model_name='test_evidence',
            name='result',
            field=models.FileField(default=False, upload_to='evidence'),
            preserve_default=False,
        ),
    ]