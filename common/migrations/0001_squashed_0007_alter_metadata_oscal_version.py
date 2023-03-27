# Generated by Django 4.1.7 on 2023-02-27 15:25

import ckeditor.fields
import common.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='addresses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('type', common.models.ShortTextField(choices=[('home', 'Home'), ('work', 'Work')], help_text='Indicates the type of address.', verbose_name='Location Type')),
                ('addr_lines', models.TextField(blank=True, help_text='All lines of an address.', max_length=1024, verbose_name='Location Address')),
                ('city', common.models.ShortTextField(blank=True, help_text='City, town or geographical region for the mailing address.', verbose_name='City')),
                ('state', common.models.ShortTextField(blank=True, help_text='State, province or analogous geographical region for mailing address', verbose_name='State')),
                ('postal_code', common.models.ShortTextField(blank=True, help_text='Postal or ZIP code for mailing address', verbose_name='Postal Code')),
                ('country', common.models.ShortTextField(blank=True, help_text='The ISO 3166-1 alpha-2 country code for the mailing address.', validators=[django.core.validators.RegexValidator(message='Must use the ISO 3166-1 alpha-2 country code', regex='[A-Z]{2}')], verbose_name='Country')),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.CreateModel(
            name='base64',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('filename', common.models.ShortTextField(help_text='Name of the file before it was encoded as Base64 to be embedded in a resource. This is the name that will be assigned to the file when the file is decoded.', verbose_name='File Name')),
                ('media_type', common.models.ShortTextField(help_text='Specifies a media type as defined by the Internet Assigned Numbers Authority (IANA) Media Types Registry.', verbose_name='Media Type')),
                ('value', models.TextField(help_text='A string representing arbitrary Base64-encoded binary data.', verbose_name='base64 encoded file')),
            ],
            options={
                'verbose_name': 'Attachment (base64)',
                'verbose_name_plural': 'Attachments (base64)',
            },
        ),
        migrations.CreateModel(
            name='citations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('text', common.models.ShortTextField(help_text='A line of citation text.', verbose_name='Citation Text')),
            ],
            options={
                'verbose_name': 'Citation',
                'verbose_name_plural': 'Citations',
            },
        ),
        migrations.CreateModel(
            name='document_ids',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('scheme', common.models.ShortTextField(blank=True, help_text='Qualifies the kind of document identifier using a URI. If the scheme is not provided the value of the element will be interpreted as a string of characters.', verbose_name='Document ID Scheme')),
                ('identifier', common.models.ShortTextField(blank=True, verbose_name='Document ID')),
            ],
            options={
                'verbose_name': 'Document ID',
                'verbose_name_plural': 'Document IDs',
            },
        ),
        migrations.CreateModel(
            name='emails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('email_address', models.EmailField(help_text='An email address as defined by RFC 5322 Section 3.4.1.', max_length=254, verbose_name='email Address')),
            ],
            options={
                'verbose_name': 'email Address',
                'verbose_name_plural': 'email Addresses',
            },
        ),
        migrations.CreateModel(
            name='external_ids',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheme', common.models.ShortTextField(help_text='Indicates the type of external identifier.', verbose_name='External Identifier Schema')),
                ('external_id', common.models.ShortTextField(blank=True, verbose_name='Party External ID')),
            ],
            options={
                'verbose_name': 'Party External Identifier',
                'verbose_name_plural': 'Party External Identifiers',
            },
        ),
        migrations.CreateModel(
            name='hashes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('algorithm', common.models.ShortTextField(help_text='Method by which a hash is derived', verbose_name='Hash algorithm')),
                ('value', models.TextField(verbose_name='Hash value')),
            ],
            options={
                'verbose_name': 'Hash',
                'verbose_name_plural': 'Hashes',
            },
        ),
        migrations.CreateModel(
            name='links',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('href', models.URLField(help_text='A resolvable URL reference to a resource.', verbose_name='Hypertext Reference')),
                ('rel', common.models.ShortTextField(blank=True, choices=[('related', 'related'), ('moved-to', 'moved-to'), ('canonical', 'canonical'), ('incorporated-into', 'incorporated-into'), ('required', 'required'), ('reference', 'reference'), ('alternate', 'alternate')], help_text="Describes the type of relationship provided by the link. This can be an indicator of the link's purpose.", verbose_name='Relation')),
                ('media_type', common.models.ShortTextField(help_text='Specifies a media type as defined by the Internet Assigned Numbers Authority (IANA) Media Types Registry (https://www.iana.org/assignments/media-types/media-types.xhtml#text).', verbose_name='Media Type')),
                ('text', common.models.ShortTextField(help_text='A textual label to associate with the link, which may be used for presentation in a tool.', verbose_name='Link Text')),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
            },
        ),
        migrations.CreateModel(
            name='locations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', models.TextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('title', common.models.ShortTextField(blank=True, help_text='A name given to the location, which may be used by a tool for display and navigation.', verbose_name='Location Title')),
                ('address', models.ForeignKey(blank=True, help_text='Typically, the physical address of the location will be used here. If this information is sensitive, then a mailing address can be used instead.', null=True, on_delete=django.db.models.deletion.CASCADE, to='common.addresses', verbose_name='Location Address')),
                ('email_addresses', common.models.CustomManyToManyField(help_text='This is a contact email associated with the location.', to='common.emails')),
                ('links', common.models.CustomManyToManyField(help_text='Links to other sites relevant to the location', to='common.links', verbose_name='Links')),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
            },
        ),
        migrations.CreateModel(
            name='organizations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
            ],
            options={
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organizations',
            },
        ),
        migrations.CreateModel(
            name='parties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', models.TextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('type', common.models.ShortTextField(choices=[('person', 'Person'), ('organization', 'Organization')], help_text='A category describing the kind of party the object describes.', verbose_name='Party Type')),
                ('name', common.models.ShortTextField(blank=True, help_text='The full name of the party. This is typically the legal name associated with the party.', verbose_name='Party Name')),
                ('short_name', common.models.ShortTextField(blank=True, help_text='A short common name, abbreviation, or acronym for the party.', verbose_name='Party Short Name')),
                ('address', models.ForeignKey(help_text='Typically, the physical address of the Party will be used here. If this information is sensitive, then a mailing address can be used instead.', null=True, on_delete=django.db.models.deletion.CASCADE, to='common.addresses', verbose_name='Location Address')),
                ('email_addresses', common.models.CustomManyToManyField(help_text='This is a contact email associated with the Party.', to='common.emails')),
                ('external_ids', common.models.CustomManyToManyField(to='common.external_ids')),
                ('links', common.models.CustomManyToManyField(to='common.links', verbose_name='Links')),
                ('location_uuids', common.models.CustomManyToManyField(help_text='References a location defined in metadata', to='common.locations', verbose_name='Party Locations')),
                ('member_of_organizations', common.models.CustomManyToManyField(help_text='Identifies that the party object is a member of the organization associated with the provided UUID.', to='common.organizations', verbose_name='Organizational Affiliations')),
            ],
            options={
                'verbose_name': 'Party',
                'verbose_name_plural': 'Parties',
            },
        ),
        migrations.CreateModel(
            name='port_ranges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('start', models.IntegerField(help_text='Indicates the starting port number in a port range', verbose_name='Start')),
                ('end', models.IntegerField(help_text='Indicates the ending port number in a port range', verbose_name='End')),
                ('transport', common.models.ShortTextField(choices=[('tcp', 'TCP'), ('udp', 'UDP')], verbose_name='Transport')),
            ],
            options={
                'verbose_name': 'Port Range',
                'verbose_name_plural': 'Port Ranges',
            },
        ),
        migrations.CreateModel(
            name='props',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('name', common.models.ShortTextField(help_text="A textual label that uniquely identifies a specific attribute, characteristic, or quality of the property's containing object.", verbose_name='Property Name')),
                ('ns', common.models.ShortTextField(default='https://csrc.nist.gov/ns/oscal', help_text="A namespace qualifying the property's name. This allows different organizations to associate distinct semantics with the same name.", verbose_name='Property Namespace')),
                ('value', common.models.ShortTextField(help_text='Indicates the value of the attribute, characteristic, or quality.', verbose_name='Property Value')),
                ('property_class', common.models.ShortTextField(blank=True, help_text="A textual label that provides a sub-type or characterization of the property's name. This can be used to further distinguish or discriminate between the semantics of multiple properties of the same object with the same name and ns.", verbose_name='Property Class')),
            ],
            options={
                'verbose_name': 'Property',
                'verbose_name_plural': 'Properties',
            },
        ),
        migrations.CreateModel(
            name='telephone_numbers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('type', common.models.ShortTextField(choices=[('home', 'Home'), ('work', 'Work'), ('mobile', 'Mobile')], help_text='Indicates the type of phone number.', verbose_name='Phone Number Type')),
                ('number', common.models.ShortTextField(help_text='Phone Number', verbose_name='Phone Number')),
            ],
            options={
                'verbose_name': 'Phone Number',
                'verbose_name_plural': 'Phone Numbers',
            },
        ),
        migrations.CreateModel(
            name='rlinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('hashes', common.models.CustomManyToManyField(help_text='A representation of a cryptographic digest generated over a resource using a specified hash algorithm.', to='common.hashes', verbose_name='Hashes')),
                ('href', common.models.CustomManyToManyField(help_text='A resolvable URI reference to a resource.', to='common.links', verbose_name='Hypertext Reference')),
            ],
            options={
                'verbose_name': 'Resource link',
                'verbose_name_plural': 'Resource links',
            },
        ),
        migrations.CreateModel(
            name='revisions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('title', common.models.ShortTextField(help_text='A name given to the document, which may be used by a tool for display and navigation.', verbose_name='Document Title')),
                ('published', models.DateTimeField(help_text='The date and time the document was published. The date-time value must be formatted according to RFC 3339 with full time and time zone included.', verbose_name='Publication Timestamp')),
                ('last_modified', models.DateTimeField(help_text='The date and time the document was last modified. The date-time value must be formatted according to RFC 3339 with full time and time zone included.', verbose_name='Last Modified Timestamp')),
                ('version', common.models.ShortTextField(help_text='A string used to distinguish the current version of the document from other previous (and future) versions.', verbose_name='Document Version')),
                ('oscal_version', common.models.ShortTextField(help_text='The OSCAL model version the document was authored against.', verbose_name='OSCAL Version')),
                ('props', common.models.properties_field(to='common.props')),
            ],
            options={
                'verbose_name': 'Revision',
                'verbose_name_plural': 'Revisions',
            },
        ),
        migrations.CreateModel(
            name='responsible_parties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('role_id', common.models.ShortTextField(help_text='The role that the party is responsible for.', verbose_name='Responsible Role')),
                ('links', common.models.CustomManyToManyField(to='common.links', verbose_name='Links')),
                ('party_uuids', common.models.CustomManyToManyField(help_text='Specifies one or more parties that are responsible for performing the associated role.', to='common.parties', verbose_name='Party Reference')),
                ('props', common.models.properties_field(to='common.props')),
            ],
            options={
                'verbose_name': 'Responsible Party',
                'verbose_name_plural': 'Responsible Parties',
            },
        ),
        migrations.CreateModel(
            name='resources',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('title', common.models.ShortTextField(help_text='A name given to the resource, which may be used by a tool for display and navigation.', verbose_name='Resource Title')),
                ('description', ckeditor.fields.RichTextField(help_text='Describes how the system satisfies a set of controls.', verbose_name='Description')),
                ('base64', common.models.CustomManyToManyField(help_text='A string representing arbitrary Base64-encoded binary data.', to='common.base64', verbose_name='Base64 encoded objects')),
                ('citation', common.models.CustomManyToManyField(help_text='A citation consisting of end note text and optional structured bibliographic data.', to='common.citations', verbose_name='Citations')),
                ('document_ids', common.models.CustomManyToManyField(help_text='A document identifier qualified by an identifier scheme. A document identifier provides a globally unique identifier for a group of documents that are to be treated as different versions of the same document.', to='common.document_ids', verbose_name='Document Identifiers')),
                ('props', common.models.properties_field(to='common.props')),
                ('rlinks', common.models.CustomManyToManyField(help_text='A pointer to an external resource with an optional hash for verification and change detection. This construct is different from link, which makes no provision for a hash or formal title.', to='common.rlinks', verbose_name='Resource link')),
            ],
            options={
                'verbose_name': 'Resource',
                'verbose_name_plural': 'Resources',
            },
        ),
        migrations.AddField(
            model_name='parties',
            name='props',
            field=common.models.properties_field(to='common.props'),
        ),
        migrations.AddField(
            model_name='parties',
            name='telephone_numbers',
            field=common.models.CustomManyToManyField(help_text='A phone number used to contact the Party.', to='common.telephone_numbers', verbose_name='Location Phone Numbers'),
        ),
        migrations.AddField(
            model_name='locations',
            name='props',
            field=common.models.properties_field(to='common.props'),
        ),
        migrations.AddField(
            model_name='locations',
            name='telephone_numbers',
            field=common.models.CustomManyToManyField(help_text='A phone number used to contact the location.', to='common.telephone_numbers', verbose_name='Location Phone Numbers'),
        ),
        migrations.AddField(
            model_name='locations',
            name='urls',
            field=common.models.CustomManyToManyField(help_text='The uniform resource locator (URL) for a web site or Internet presence associated with the location.', related_name='location_urls', to='common.links', verbose_name='Location URLs'),
        ),
        migrations.AddField(
            model_name='citations',
            name='links',
            field=common.models.CustomManyToManyField(to='common.links', verbose_name='Links'),
        ),
        migrations.AddField(
            model_name='citations',
            name='props',
            field=common.models.properties_field(to='common.props'),
        ),
        migrations.AlterField(
            model_name='locations',
            name='remarks',
            field=ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks'),
        ),
        migrations.AlterField(
            model_name='parties',
            name='remarks',
            field=ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks'),
        ),
        migrations.CreateModel(
            name='back_matter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('resources', common.models.CustomManyToManyField(help_text='A resource associated with content in the containing document. A resource may be directly included in the document base64 encoded or may point to one or more equivalent internet resources.', to='common.resources', verbose_name='Resources')),
            ],
            options={
                'verbose_name': 'Back matter',
                'verbose_name_plural': 'Back matter',
            },
        ),
        migrations.CreateModel(
            name='protocols',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('name', common.models.ShortTextField(help_text='The common name of the protocol, which should be the appropriate service name from the IANA Service Name and Transport Protocol Port Number Registry', verbose_name='Protocol Name')),
                ('title', common.models.ShortTextField(help_text='A human readable name for the protocol (e.g., Transport Layer Security).', verbose_name='Protocol Title')),
                ('port_ranges', common.models.CustomManyToManyField(to='common.port_ranges', verbose_name='Port Ranges')),
            ],
            options={
                'verbose_name': 'Protocol',
                'verbose_name_plural': 'Protocols',
            },
        ),
        migrations.CreateModel(
            name='roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('role_id', common.models.ShortTextField(help_text="A unique identifSorry to cancel last minuteSier for a specific role instance. This identifier's uniqueness is document scoped and is intended to be consistent for the same role across minor revisions of the document.", verbose_name='Role ID')),
                ('title', common.models.ShortTextField(help_text='A name given to the role, which may be used by a tool for display and navigation.', verbose_name='Role Title')),
                ('short_name', common.models.ShortTextField(blank=True, help_text='A short common name, abbreviation, or acronym for the role.', verbose_name='Role Short Name')),
                ('description', ckeditor.fields.RichTextField(blank=True, help_text="A summary of the role's purpose and associated responsibilities.", verbose_name='Role Description')),
                ('links', common.models.CustomManyToManyField(to='common.links', verbose_name='Role Links')),
                ('props', common.models.properties_field(to='common.props')),
            ],
            options={
                'verbose_name': 'System Role',
                'verbose_name_plural': 'System Roles',
            },
        ),
        migrations.CreateModel(
            name='metadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', ckeditor.fields.RichTextField(blank=True, default='', help_text='Additional commentary on the containing object.', verbose_name='Remarks')),
                ('title', common.models.ShortTextField(help_text='A name given to the document, which may be used by a tool for display and navigation.', verbose_name='Document Title')),
                ('published', models.DateTimeField(help_text='The date and time the document was published. The date-time value must be formatted according to RFC 3339 with full time and time zone included.', null=True, verbose_name='Publication Timestamp')),
                ('last_modified', models.DateTimeField(default=django.utils.timezone.now, help_text='The date and time the document was last modified. The date-time value must be formatted according to RFC 3339 with full time and time zone included.', verbose_name='Last Modified Timestamp')),
                ('version', common.models.ShortTextField(default='1.0', help_text='A string used to distinguish the current version of the document from other previous (and future) versions.', verbose_name='Document Version')),
                ('oscal_version', common.models.ShortTextField(default='v1.0.3', help_text='The OSCAL model version the document was authored against.', verbose_name='OSCAL Version')),
                ('document_ids', common.models.CustomManyToManyField(to='common.document_ids', verbose_name='Other Document IDs')),
                ('links', common.models.CustomManyToManyField(to='common.links', verbose_name='Links')),
                ('locations', common.models.CustomManyToManyField(to='common.locations', verbose_name='Locations')),
                ('parties', common.models.CustomManyToManyField(help_text='A responsible entity which is either a person or an organization.', to='common.parties', verbose_name='Parties (organizations or persons)')),
                ('props', common.models.properties_field(to='common.props')),
                ('responsible_parties', common.models.CustomManyToManyField(help_text=' A reference to a set of organizations or persons that have responsibility for performing a referenced role in the context of the containing object.', to='common.responsible_parties', verbose_name='Responsible Parties')),
                ('revisions', common.models.CustomManyToManyField(to='common.revisions', verbose_name='Previous Revisions')),
            ],
            options={
                'verbose_name': 'Metadata',
                'verbose_name_plural': 'Metadata',
            },
        ),
    ]
