# Generated by Django 4.2.5 on 2023-12-08 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0011_alter_metadata_document_ids_alter_metadata_locations_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='back_matter',
            name='resources',
            field=models.ManyToManyField(blank=True, help_text='A resource associated with content in the containing document. A resource may be directly included in the document base64 encoded or may point to one or more equivalent internet resources.', to='common.resources', verbose_name='Resources'),
        ),
        migrations.AlterField(
            model_name='locations',
            name='email_addresses',
            field=models.ManyToManyField(blank=True, help_text='This is a contact email associated with the location.', to='common.emails'),
        ),
        migrations.AlterField(
            model_name='locations',
            name='links',
            field=models.ManyToManyField(blank=True, help_text='Links to other sites relevant to the location', to='common.links', verbose_name='Links'),
        ),
        migrations.AlterField(
            model_name='locations',
            name='telephone_numbers',
            field=models.ManyToManyField(blank=True, help_text='A phone number used to contact the location.', to='common.telephone_numbers', verbose_name='Location Phone Numbers'),
        ),
        migrations.AlterField(
            model_name='locations',
            name='urls',
            field=models.ManyToManyField(blank=True, help_text='The uniform resource locator (URL) for a web site or Internet presence associated with the location.', related_name='location_urls', to='common.links', verbose_name='Location URLs'),
        ),
        migrations.AlterField(
            model_name='parties',
            name='email_addresses',
            field=models.ManyToManyField(blank=True, help_text='This is a contact email associated with the Party.', to='common.emails'),
        ),
        migrations.AlterField(
            model_name='parties',
            name='external_ids',
            field=models.ManyToManyField(blank=True, to='common.external_ids'),
        ),
        migrations.AlterField(
            model_name='parties',
            name='location_uuids',
            field=models.ManyToManyField(blank=True, help_text='References a location defined in metadata', to='common.locations', verbose_name='Party Locations'),
        ),
        migrations.AlterField(
            model_name='parties',
            name='member_of_organizations',
            field=models.ManyToManyField(blank=True, help_text='Identifies that the party object is a member of the organization associated with the provided UUID.', to='common.organizations', verbose_name='Organizational Affiliations'),
        ),
        migrations.AlterField(
            model_name='parties',
            name='telephone_numbers',
            field=models.ManyToManyField(blank=True, help_text='A phone number used to contact the Party.', to='common.telephone_numbers', verbose_name='Location Phone Numbers'),
        ),
        migrations.AlterField(
            model_name='resources',
            name='base64',
            field=models.ManyToManyField(blank=True, help_text='A string representing arbitrary Base64-encoded binary data.', to='common.base64', verbose_name='Base64 encoded objects'),
        ),
        migrations.AlterField(
            model_name='resources',
            name='citation',
            field=models.ManyToManyField(blank=True, help_text='A citation consisting of end note text and optional structured bibliographic data.', to='common.citations', verbose_name='Citations'),
        ),
        migrations.AlterField(
            model_name='resources',
            name='document_ids',
            field=models.ManyToManyField(blank=True, help_text='A document identifier qualified by an identifier scheme. A document identifier provides a globally unique identifier for a group of documents that are to be treated as different versions of the same document.', to='common.document_ids', verbose_name='Document Identifiers'),
        ),
        migrations.AlterField(
            model_name='resources',
            name='rlinks',
            field=models.ManyToManyField(blank=True, help_text='A pointer to an external resource with an optional hash for verification and change detection. This construct is different from link, which makes no provision for a hash or formal title.', to='common.rlinks', verbose_name='Resource link'),
        ),
        migrations.AlterField(
            model_name='responsible_parties',
            name='party_uuids',
            field=models.ManyToManyField(blank=True, help_text='Specifies one or more parties that are responsible for performing the associated role.', to='common.parties', verbose_name='Party Reference'),
        ),
        migrations.AlterField(
            model_name='rlinks',
            name='hashes',
            field=models.ManyToManyField(blank=True, help_text='A representation of a cryptographic digest generated over a resource using a specified hash algorithm.', to='common.hashes', verbose_name='Hashes'),
        ),
    ]