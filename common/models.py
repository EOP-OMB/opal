import logging
from django.db import models, IntegrityError, connection, OperationalError
from django.core.validators import RegexValidator
import uuid
from itertools import chain
from django.utils.timezone import now
from common.functions import replace_hyphen, search_for_uuid
from django.core.exceptions import ObjectDoesNotExist  # ValidationError
from django.urls import reverse


class ShortTextField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 1024
        kwargs['default'] = ""
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        del kwargs['default']
        return name, path, args, kwargs


class CustomManyToManyField(models.ManyToManyField):
    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        # kwargs['null'] = True
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['blank']
        # del kwargs['null']
        return name, path, args, kwargs

    def first(self):
        pass


class propertiesField(CustomManyToManyField):
    def __init__(self, *args, **kwargs):
        kwargs['to'] = "common.props"
        kwargs['verbose_name'] = "Properties"
        kwargs[
            'help_text'] = "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair. The value of a property is a simple scalar value, which may be expressed as a list of values."
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # del kwargs['to']
        del kwargs['verbose_name']
        del kwargs['help_text']
        return name, path, args, kwargs


system_status_state_choices = [
    ("operational", "Operational: The system or component is currently operating in production."),
    ("under-development", "Under Development: The system or component is being designed, developed, or implemented"), (
        "under-major-modification",
        "Under Major Modification: The system or component is undergoing a major change, development, or transition."),
    ("disposition", "Disposition: The system or component is no longer operational."),
    ("other", "Other: Some other state, a remark must be included to describe the current state.")]

implementation_status_choices = [
    ("implemented", "Implemented: The control is fully implemented."),
    ("partial", "Partial: The control is partially implemented."),
    ("planned", "Planned: There is a plan for implementing the control as explained in the remarks."),
    ("alternative","Alternative: There is an alternative implementation for this control as explained in the remarks.",),
    ("not-applicable","Not-Applicable: This control does not apply to this system as justified in the remarks.",)
    ]


class PrimitiveModel(models.Model):
    uuid = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        get_latest_by = "updated_at"

    def natural_key(self):
        return self.uuid

    def get_permalink(self):
        url = reverse('common:permalink', kwargs={'p_uuid': str(self.uuid)})
        return url

    def get_absolute_url(self):
        admin_str = 'admin:' + "_".join([self._meta.app_label, self._meta.model_name, 'change'])
        change_url = reverse(admin_str, args=(self.id,))
        return change_url

    def to_dict(self):
        opts = self._meta
        excluded_fields = ['id', 'pk', 'created_at', 'updated_at', 'uuid']
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields):
            if f.name not in excluded_fields:
                if f.get_internal_type() == 'ForeignKey':
                    child = self.__getattribute__(f.name)
                    if child is not None:
                        data[f.name] = child.to_dict()
                else:
                    data[f.name] = f.value_to_string(self)
        for f in opts.many_to_many:
            data[f.name] = [i.to_dict() for i in f.value_from_object(self)]
        return data

    def to_html(self):
        logger = logging.getLogger('django')
        opts = self._meta
        # list of some excluded fields
        excluded_fields = ['id', 'pk', 'created_at', 'updated_at', 'uuid']

        html_str = "\n"
        # getting all fields that available in `Client` model,
        # but not in `excluded_fields`
        for f in opts.concrete_fields:
            if f.name not in excluded_fields:
                if f.get_internal_type() == 'ForeignKey':
                    child = self.__getattribute__(f.name)
                    if child is not None:
                        value = child.to_html()
                    else:
                        value = None
                else:
                    if f.value_to_string(self) != "":
                        value = f.value_to_string(self)
                    else:
                        value = None
                if value is not None:
                    html_str += "<li>" + f.verbose_name + ": " + value + "</li>\n"
        for f in opts.many_to_many:
            if len(f.value_from_object(self)) > 0:
                html_str += "<li>" + f.verbose_name + ":</li>\n"
                for i in f.value_from_object(self):
                    html_str += i.to_html()
        html_str += "</ul>\n"
        if html_str is None:
            html_str = "None"
        return html_str

    def field_name_changes(self):
        return {}

    def fix_field_names(self, d):
        new_dict = {}
        del_keys = set()
        if type(d) is dict:
            if len(self.field_name_changes()) == 0:
                # No specific field list, just fix the hyphens
                for k in d:
                    if "-" in k:
                        new_key = replace_hyphen(k)
                        new_dict[new_key] = d[k]
                        del_keys.add(k)
            else:
                # if object has a custom list it will include any hyphens
                name_change_list: dict = self.field_name_changes()
                if type(name_change_list) is dict:
                    for k in d:
                        if k in name_change_list:
                            new_key = name_change_list[k]
                            new_dict[new_key] = d[k]
                            del_keys.add(k)
            for k in del_keys:
                d.pop(k)
            merged_dict = {**new_dict, **d}
        else:
            merged_dict = d
        return merged_dict

    def import_oscal(self, oscal_data):
        logger = logging.getLogger("django")
        opts = self._meta
        logger.info("Starting import for " + opts.model_name)
        if oscal_data is None or len(oscal_data) == 0:
            logger.error("oscal_data is 0 length")
        excluded_fields = ['id', 'pk', 'created_at', 'updated_at']
        field_list = list(opts.concrete_fields)
        field_list_str = []
        logger.info("Removing excluded fields from field_list")
        for f in field_list:
            if f.name in excluded_fields:
                field_list.remove(f)
            else:
                field_list_str.append(f.name)
        logger.info("model = " + opts.model_name)
        logger.info("field_list = " + ', '.join(field_list_str))
        if type(oscal_data) is dict:
            logger.info("Handling dictionary...")
            # replace field names to match internal model names
            oscal_data = self.fix_field_names(oscal_data)
            if "uuid" in oscal_data.keys():
                # check to see if the object already exists
                logger.info("Checking for an existing " + opts.model_name + " with uuid " + oscal_data["uuid"])
                if opts.model.objects.filter(uuid=oscal_data["uuid"]).exists():
                    logger.info("Found an existing " + opts.model_name + " with uuid " + oscal_data["uuid"])
                    old_obj = opts.model.objects.get(uuid=oscal_data["uuid"])
                    old_obj.delete()
                    logger.info("Deleted existing " + opts.model_name + " with uuid " + oscal_data["uuid"])
                else:
                    logger.info("Could not find an existing " + opts.model_name + " with uuid " + oscal_data["uuid"])
            for f in field_list:
                if f.name in oscal_data.keys():
                    if f.get_internal_type() == 'ForeignKey':
                        logger.info(f.name + " is a foreign key. Creating child object...")
                        child = f.related_model()
                        child = child.import_oscal(oscal_data[f.name])
                        self.__setattr__(f.name, child)
                        logger.info("Created new " + f.name + " with id " + str(child.id))
                    else:
                        field = f.name
                        value = oscal_data[f.name]
                        if type(value) is str:
                            logger.info("Setting " + field + " to " + value)
                            self.__setattr__(field, value)
                        else:
                            logger.warning(field + " value is a " + str(type(value)))
                        logger.info("Done")
        elif type(oscal_data) is str:
            logger.info("Handling string...")
            # maybe the model has just one field?
            if 'uuid' in field_list:
                copy_field_list = field_list.copy()
                copy_field_list.remove('uuid')
                if len(copy_field_list) == 1:
                    field = field_list[0]
                    value = oscal_data
                    self.__setattr__(field,value)
                else:
                    uuid_obj = False
                    try:
                        uuid_obj = uuid.UUID(oscal_data, version=4)
                    except ValueError:
                        logger.info(oscal_data + " is not a valid uuid")
                    if uuid_obj:
                        if opts.model.objects.filter(uuid=uuid_obj).exists:
                            logger.info("Found a " + opts.model_name + " with uuid " + oscal_data)
                        else:
                            logger.info("Could not find an existing " + opts.model_name + " with uuid " + oscal_data)
                            logger.info("Creating a new " + opts.model_name + " with uuid " + oscal_data)
                            field = 'uuid'
                            value = uuid_obj
                            self.__setattr__(field, value)
            else:
                logger.error("oscal_data does not provide a field name. " + opts.model_name + " with oscal_data " + oscal_data)
        else:
            logger.error("oscal_data is not a dictionary, string, or list.  oscal_data:")
            logger.error(oscal_data)
        self.save()
        logger.info('Handling the many_to_many fields')
        field_list = list(opts.many_to_many)
        logger.info("field_list = " + ', '.join(field_list_str))
        if type(oscal_data) is dict:
            for f in field_list:
                if f.name in oscal_data.keys():
                    if type(oscal_data[f.name]) is dict and len(oscal_data) > 0:
                        logger.info("Creating child object for field " + f.name)
                        child = f.related_model()
                        child = child.import_oscal(oscal_data[f.name])
                        self.oscal_import_save_m2m(child, f, opts)
                        logger.info("Created new " + child._meta.model_name + " with id " + str(child.id) + " and linked it to " + f.name )
                    elif type(oscal_data[f.name]) is list and len(oscal_data[f.name]) > 0:
                        for item in oscal_data[f.name]:
                            logger.info("Creating child object for field " + f.name)
                            child = f.related_model()
                            child = child.import_oscal(item)
                            self.oscal_import_save_m2m(child, f, opts)
                            logger.info("Created new " + child._meta.model_name + " with id " + str(child.id) + " and linked it to " + f.name)
                    elif type(oscal_data[f.name]) is str:
                        logger.info("Creating child object for field " + f.name)
                        child = f.related_model()
                        child = child.import_oscal(oscal_data)
                        self.oscal_import_save_m2m(child, f, opts)
                        logger.info("Created new " + child._meta.model_name + " with id " + str(child.id) + " and linked it to " + f.name)
                    else:
                        child = None
                    self.save()
                elif type(oscal_data) is str:
                    logger.info("Creating child object for field " + f.name)
                    field = f.name
                    value = oscal_data
                    self.__setattr__(field, value)
                    self.save()
                    logger.info("Created new " + child._meta.model_name + " with id " + str(child.id) + " and linked it to " + f.name)
        self.save()
        logger.info("Completed import for " + opts.model_name)
        return self

    def oscal_import_save_m2m(self, child, f, opts):
        logger = logging.getLogger("django")
        if child is not None:
            error = False
            try:
                child.save()
            except IntegrityError:
                try:
                    existing_child = child._meta.model.objects.get(uuid=child.uuid)
                    child = existing_child
                except ObjectDoesNotExist:
                    logger.error("Integrity error occurred but no matching object found with the same uuid")
                    error = True
            if self.id is None:
                logger.info("Parent id is None")
                try:
                    self.save()
                except IntegrityError as err:
                    logger.error(err)
                    error = True
            if child.id is None:
                logger.info("Child id is none")
                try:
                    child.save()
                except IntegrityError as err:
                    logger.error(err)
                    error = True
            if not error:
                parent_id = self.id
                parent_field_name = opts.model_name + "_id"
                child_id = child.id
                child_field_name = child._meta.model_name + "_id"
                if parent_field_name == child_field_name:
                    child_field_name = "to_" + child_field_name
                    parent_field_name = "from_" + parent_field_name
                table_name = f.m2m_db_table()
                sql = "INSERT INTO " + table_name + " (" + parent_field_name + "," + child_field_name + ") VALUES(" + str(
                    parent_id
                    ) + "," + str(child_id) + ")"
                with connection.cursor() as cursor:
                    try:
                        cursor.execute(sql)
                    except IntegrityError:
                        logger.info("Relationship already exists. sql = " + sql)
                    except OperationalError as err:
                        logger.error("An error occurred")
                        logger.error(err)
        return child

    def update(self, d):
        """
        Updates all fields defined in dict d
        :param d: dictionary
        :return: self
        """
        for k in d.keys():
            if k in self._meta.get_fields():
                self.__setattr__(k, d[k])
        self.save()
        return self

    def __str__(self):
        if self.uuid is None:
            uuid_str = "None"
        else:
            uuid_str = str(self.uuid)
        return str(self._meta.model_name + ": " + uuid_str)


class BasicModel(PrimitiveModel):
    remarks = models.TextField(
        verbose_name="Remarks", help_text="Additional commentary on the containing object.", blank=True, default=""
        )

    class Meta:
        abstract = True


class port_ranges(BasicModel):
    """
    Where applicable this is the IPv4 port range on which the service operates. To be validated as a natural number (integer >= 1). A single port uses the same value for start and end. Use multiple 'port-range' entries for non-contiguous ranges.
    """

    class Meta:
        verbose_name = "Port Range"
        verbose_name_plural = "Port Ranges"

    start = models.IntegerField(help_text="Indicates the starting port number in a port range", verbose_name="Start")
    end = models.IntegerField(help_text="Indicates the ending port number in a port range", verbose_name="End")
    transport = ShortTextField(max_length=3, verbose_name="Transport", choices=[('tcp', 'TCP'), ('udp', 'UDP')])

    def __str__(self):
        r = str(self.start) + '-' + str(self.end) + ' ' + self.transport
        return r


class protocols(BasicModel):
    """
     Information about the protocol used to provide a service.
    """

    class Meta:
        verbose_name = "Protocol"
        verbose_name_plural = "Protocols"

    name = ShortTextField(
        verbose_name="Protocol Name",
        help_text='The common name of the protocol, which should be the appropriate service name from the IANA Service Name and Transport Protocol Port Number Registry'
        )
    title = ShortTextField(
        verbose_name="Protocol Title",
        help_text="A human readable name for the protocol (e.g., Transport Layer Security)."
        )
    port_ranges = CustomManyToManyField(to=port_ranges, verbose_name="Port Ranges")


class props(BasicModel):
    """
    An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair. The value of a property is a simple scalar value, which may be expressed as a list of values.
    """

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"

    name = ShortTextField(
        verbose_name="Property Name",
        help_text="A textual label that uniquely identifies a specific attribute, characteristic, or quality of the property's containing object."
        )
    ns = ShortTextField(
        verbose_name="Property Namespace",
        help_text="A namespace qualifying the property's name. This allows different organizations to associate distinct semantics with the same name.",
        default="https://csrc.nist.gov/ns/oscal"
        )
    value = ShortTextField(
        verbose_name="Property Value", help_text="Indicates the value of the attribute, characteristic, or quality."
        )
    property_class = ShortTextField(
        verbose_name="Property Class",
        help_text="A textual label that provides a sub-type or characterization of the property's name. This can be used to further distinguish or discriminate between the semantics of multiple properties of the same object with the same name and ns.",
        blank=True
        )

    def __str__(self):
        return self.name + " : " + self.value


class links(BasicModel):
    """
    A reference to a local or remote resource
    """

    class Meta:
        verbose_name = "Link"
        verbose_name_plural = "Links"

    href = models.URLField(verbose_name="Hypertext Reference", help_text="A resolvable URL reference to a resource.")
    rel = ShortTextField(
        verbose_name="Relation",
        help_text="Describes the type of relationship provided by the link. This can be an indicator of the link's purpose.",
        blank=True
        )
    media_type = ShortTextField(
        verbose_name="Media Type",
        help_text="Specifies a media type as defined by the Internet Assigned Numbers Authority (IANA) Media Types Registry (https://www.iana.org/assignments/media-types/media-types.xhtml#text)."
        )
    text = ShortTextField(
        verbose_name="Link Text",
        help_text="A textual label to associate with the link, which may be used for presentation in a tool."
        )

    def __str__(self):
        return self.text

    def import_oscal(self, oscal_data):
        for k in oscal_data:
            self.__setattr__(k, oscal_data[k])
        self.save()
        return self

    def to_html(self):
        # html_str = "<a href='% s' target=_blank>% s</a>" % self.href, self.text
        if len(self.href) > 0:
            if self.rel == "reference":
                obj = search_for_uuid(self.href[1:])
                if obj is not None:
                    html_str = obj.to_html()
                else:
                    html_str = "<!-- Could not find an object matching uuid " + self.href[1:] + " in the database -->"
            else:
                if len(self.text) > 0:
                    href_text = self.text
                else:
                    href_text = self.href
                html_str = "<a href='" + self.href + "' target=_blank>" + href_text + "</a>"
        else:
            html_str = ""
        return html_str


class revisions(BasicModel):
    """
    An entry in a sequential list of revisions to the containing document in reverse chronological order (i.e., most recent previous revision first).
    """

    class Meta:
        verbose_name = "Revision"
        verbose_name_plural = "Revisions"

    title = ShortTextField(
        verbose_name="Document Title",
        help_text="A name given to the document, which may be used by a tool for display and navigation."
        )
    published = models.DateTimeField(
        verbose_name="Publication Timestamp",
        help_text="The date and time the document was published. The date-time value must be formatted according to RFC 3339 with full time and time zone included."
        )
    last_modified = models.DateTimeField(
        verbose_name="Last Modified Timestamp",
        help_text="The date and time the document was last modified. The date-time value must be formatted according to RFC 3339 with full time and time zone included."
        )
    version = ShortTextField(
        verbose_name="Document Version",
        help_text="A string used to distinguish the current version of the document from other previous (and future) versions."
        )
    oscal_version = ShortTextField(
        verbose_name="OSCAL Version", help_text="The OSCAL model version the document was authored against."
        )
    props = propertiesField()


class document_ids(PrimitiveModel):
    """
    A document identifier qualified by an identifier scheme. A document identifier provides a globally unique identifier for a group of documents that are to be treated as different versions of the same document. If this element does not appear, or if the value of this element is empty, the value of "document-id" is equal to the value of the "uuid" flag of the top-level root element.
    Remarks
    This element is optional, but it will always have a valid value, as if it is missing the value of "document-id" is assumed to be equal to the UUID of the root. This requirement allows for document creators to retroactively link an update to the original version, by providing a document-id on the new document that is equal to the uuid of the original document.
    """

    class Meta:
        verbose_name = "Document ID"
        verbose_name_plural = "Document IDs"

    scheme = ShortTextField(
        verbose_name="Document ID Scheme",
        help_text="Qualifies the kind of document identifier using a URI. If the scheme is not provided the value of the element will be interpreted as a string of characters.",
        blank=True
        )
    identifier = ShortTextField(verbose_name="Document ID", help_text="", blank=True)

    def __str__(self):
        return self.scheme + " - " + self.identifier


class roles(BasicModel):
    """
    Defines a function assumed or expected to be assumed by a party in a specific situation.
    """

    class Meta:
        verbose_name = "System Role"
        verbose_name_plural = "System Roles"

    role_id = ShortTextField(
        verbose_name="Role ID",
        help_text="A unique identifSorry to cancel last minuteSier for a specific role instance. This identifier's uniqueness is document scoped and is intended to be consistent for the same role across minor revisions of the document."
        )
    title = ShortTextField(
        verbose_name="Role Title",
        help_text="A name given to the role, which may be used by a tool for display and navigation."
        )
    short_name = ShortTextField(
        verbose_name="Role Short Name", help_text="A short common name, abbreviation, or acronym for the role.",
        blank=True
        )
    description = models.TextField(
        verbose_name="Role Description", help_text="A summary of the role's purpose and associated responsibilities.",
        blank=True
        )
    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Role Links")


    def __str__(self):
        return self.title


    def import_oscal(self, oscal_data):
        if type(oscal_data) is str:
            self.role_id = oscal_data
        elif type(oscal_data) is dict:
            if "role_id" in oscal_data.keys():
                self.role_id = oscal_data["role_id"]
            if "title" in oscal_data.keys():
                self.title = oscal_data["title"]
            if "short_name" in oscal_data.keys():
                self.title = oscal_data["short_name"]
            if "description" in oscal_data.keys():
                self.title = oscal_data["description"]
            if "props" in oscal_data.keys():
                for item in oscal_data["props"]:
                    child = props()
                    child.import_oscal(item)
                    self.save()
            if "links" in oscal_data.keys():
                for item in oscal_data["links"]:
                    child = links()
                    child.import_oscal(item)
                    self.save()
        self.save()
        return self


class emails(BasicModel):
    """
    An email address as defined by RFC 5322 Section 3.4.1.
    """

    class Meta:
        verbose_name = "email Address"
        verbose_name_plural = "email Addresses"

    email_address = models.EmailField(
        verbose_name="email Address", help_text="An email address as defined by RFC 5322 Section 3.4.1."
        )

    def import_oscal(self, oscal_data):
        self.email_address = oscal_data
        self.save()
        return self

    def __str__(self):
        return self.email_address


class telephone_numbers(BasicModel):
    """
    Contact number by telephone.
    """

    class Meta:
        verbose_name = "Phone Number"
        verbose_name_plural = "Phone Numbers"

    type = ShortTextField(
        verbose_name="Phone Number Type", help_text="Indicates the type of phone number.",
        choices=[("home", "Home"), ("work", "Work"), ("mobile", "Mobile")]
        )
    number = ShortTextField(verbose_name="Phone Number", help_text="Phone Number")

    def __str__(self):
        return self.type + ": " + self.number


class addresses(BasicModel):
    """
    Typically, the physical address of the location will be used here. If this information is sensitive, then a mailing address can be used instead.
    """

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    type = ShortTextField(
        verbose_name="Location Type", help_text="Indicates the type of address.",
        choices=[("home", "Home"), ("work", "Work")]
        )
    addr_lines = models.TextField(
        max_length=1024, verbose_name="Location Address", help_text="All lines of an address.", blank=True
        )
    city = ShortTextField(
        verbose_name="City", help_text="City, town or geographical region for the mailing address.", blank=True
        )
    state = ShortTextField(
        verbose_name="State", help_text="State, province or analogous geographical region for mailing address",
        blank=True
        )
    postal_code = ShortTextField(
        verbose_name="Postal Code", help_text="Postal or ZIP code for mailing address", blank=True
        )
    country = ShortTextField(
        verbose_name="Country", help_text="The ISO 3166-1 alpha-2 country code for the mailing address.", blank=True,
        max_length=2, validators=[RegexValidator(
            regex='[A-Z]{2}', message="Must use the ISO 3166-1 alpha-2 country code"
            )]
        )

    def __str__(self):
        return ", ".join([self.addr_lines, self.city, self.state])


class locations(BasicModel):
    """
    A location, with associated metadata that can be referenced.
    """

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    title = ShortTextField(
        verbose_name="Location Title",
        help_text="A name given to the location, which may be used by a tool for display and navigation.", blank=True
        )
    address = models.ForeignKey(
        to=addresses, verbose_name="Location Address",
        help_text="Typically, the physical address of the location will be used here. If this information is sensitive, then a mailing address can be used instead.",
        blank=True, null=True, on_delete=models.CASCADE
        )
    email_addresses = CustomManyToManyField(
        to=emails, help_text="This is a contact email associated with the location."
        )
    telephone_numbers = CustomManyToManyField(
        to=telephone_numbers, verbose_name="Location Phone Numbers",
        help_text="A phone number used to contact the location."
        )
    urls = CustomManyToManyField(
        to=links, verbose_name="Location URLs",
        help_text="The uniform resource locator (URL) for a web site or Internet presence associated with the location.",
        related_name="location_urls"
        )
    props = propertiesField()
    links = CustomManyToManyField(
        to=links, verbose_name="Links", help_text="Links to other sites relevant to the location"
        )


class external_ids(models.Model):
    """
    An identifier for a person or organization using a designated scheme. e.g. an Open Researcher and Contributor ID (ORCID)
    """

    class Meta:
        verbose_name = "Party External Identifier"
        verbose_name_plural = "Party External Identifiers"

    scheme = ShortTextField(
        verbose_name="External Identifier Schema", help_text="Indicates the type of external identifier."
        )
    external_id = ShortTextField(verbose_name="Party External ID", blank=True)

    def __str__(self):
        return self.scheme + " - " + self.external_id


class organizations(BasicModel):
    """

    """

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"


class parties(BasicModel):
    """
    A responsible entity which is either a person or an organization.
    """

    class Meta:
        verbose_name = "Party"
        verbose_name_plural = "Parties"

    type = ShortTextField(
        verbose_name="Party Type", help_text="A category describing the kind of party the object describes.",
        choices=[("person", "Person"), ("organization", "Organization")]
        )
    name = ShortTextField(
        verbose_name="Party Name",
        help_text="The full name of the party. This is typically the legal name associated with the party.", blank=True
        )
    short_name = ShortTextField(
        verbose_name="Party Short Name", help_text="A short common name, abbreviation, or acronym for the party.",
        blank=True
        )
    external_ids = CustomManyToManyField(to=external_ids)
    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    address = models.ForeignKey(
        to=addresses, verbose_name="Location Address",
        help_text="Typically, the physical address of the Party will be used here. If this information is sensitive, then a mailing address can be used instead.",
        on_delete=models.CASCADE, null=True
        )
    email_addresses = CustomManyToManyField(
        to=emails, help_text="This is a contact email associated with the Party."
        )
    telephone_numbers = CustomManyToManyField(
        to=telephone_numbers, verbose_name="Location Phone Numbers",
        help_text="A phone number used to contact the Party."
        )
    location_uuids = CustomManyToManyField(
        to=locations, verbose_name="Party Locations", help_text="References a location defined in metadata"
        )
    member_of_organizations = CustomManyToManyField(
        to=organizations, verbose_name="Organizational Affiliations",
        help_text="Identifies that the party object is a member of the organization associated with the provided UUID.", )

    def __str__(self):
        return self.name


class responsible_parties(PrimitiveModel):
    """
     A reference to a set of organizations or persons that have responsibility for performing a referenced role in the context of the containing object.
    """

    class Meta:
        verbose_name = "Responsible Party"
        verbose_name_plural = "Responsible Parties"

    role_id = ShortTextField(
        verbose_name="Responsible Role", help_text="The role that the party is responsible for."
        )
    party_uuids = CustomManyToManyField(
        to=parties, verbose_name="Party Reference",
        help_text="Specifies one or more parties that are responsible for performing the associated role."
        )
    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")

    def field_name_changes(self):
        field_name_changes = {
            "id": "role_id", "uuid": "party_uuids"
            }
        return field_name_changes

    def __str__(self):
        parties_list = []
        for item in self.party_uuids.all():
            parties_list.append(item.name)
        if len(parties_list) > 0:
            return_str = ", ".join(parties_list)
        else:
            return_str = "N/A"
        if self.role_id is not None:
            return_str = str(self.role_id) + ": " + return_str
        return return_str


class metadata(BasicModel):
    """
    Provides information about the publication and availability of the containing document.
    """

    class Meta:
        verbose_name = "Metadata"
        verbose_name_plural = "Metadata"

    title = ShortTextField(
        verbose_name="Document Title",
        help_text="A name given to the document, which may be used by a tool for display and navigation."
        )
    published = models.DateTimeField(
        verbose_name="Publication Timestamp",
        help_text="The date and time the document was published. The date-time value must be formatted according to RFC 3339 with full time and time zone included.",
        null=True
        )
    last_modified = models.DateTimeField(
        verbose_name="Last Modified Timestamp",
        help_text="The date and time the document was last modified. The date-time value must be formatted according to RFC 3339 with full time and time zone included.",
        default=now
        )
    version = ShortTextField(
        verbose_name="Document Version",
        help_text="A string used to distinguish the current version of the document from other previous (and future) versions.",
        default="1.0"
        )
    oscal_version = ShortTextField(
        verbose_name="OSCAL Version", help_text="The OSCAL model version the document was authored against.",
        default="1.0.0"
        )
    revisions = CustomManyToManyField(to=revisions, verbose_name="Previous Revisions")
    document_ids = CustomManyToManyField(to=document_ids, verbose_name="Other Document IDs")
    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    locations = CustomManyToManyField(to=locations, verbose_name="Locations")
    parties = CustomManyToManyField(
        to=parties, verbose_name="Parties (organizations or persons)",
        help_text="A responsible entity which is either a person or an organization."
        )
    responsible_parties = CustomManyToManyField(
        to=responsible_parties, verbose_name="Responsible Parties",
        help_text=" A reference to a set of organizations or persons that have responsibility for performing a referenced role in the context of the containing object."
        )


class citations(PrimitiveModel):
    """
    A citation consisting of end note text and optional structured bibliographic data.
    """

    class Meta:
        verbose_name = "Citation"
        verbose_name_plural = "Citations"

    text = ShortTextField(verbose_name="Citation Text", help_text="A line of citation text.")
    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")

    def import_oscal(self, oscal_data):
        if type(oscal_data) is dict:
            if "text" in oscal_data.keys():
                self.text = oscal_data["text"]
            if "links" in oscal_data.keys():
                for l in oscal_data["links"]:
                    child = links()
                    child = child.import_oscal(l)
                    if child is not None:
                        child.save()
                        self.links.add(child.id)
                        self.save()
            if "props" in oscal_data.keys():
                for p in oscal_data["props"]:
                    child = props()
                    child = child.import_oscal(p)
                    if child is not None:
                        child.save()
                        self.props.add(child.id)
                        self.save()
        else:
            self.text = oscal_data
        self.save()
        return self


class hashes(PrimitiveModel):
    """
    A representation of a cryptographic digest generated over a resource using a specified hash algorithm.
    """

    class Meta:
        verbose_name = "Hash"
        verbose_name_plural = "Hashes"

    algorithm = ShortTextField(verbose_name="Hash algorithm", help_text="Method by which a hash is derived")
    value = models.TextField(verbose_name="Hash value")


class rlinks(PrimitiveModel):
    """
    A pointer to an external resource with an optional hash for verification and change detection. This construct is different from link, which makes no provision for a hash or formal title.
    """

    class Meta:
        verbose_name = "Resource link"
        verbose_name_plural = "Resource links"

    href = CustomManyToManyField(
        to=links, verbose_name="Hypertext Reference", help_text="A resolvable URI reference to a resource."
        )
    hashes = CustomManyToManyField(
        to=hashes, verbose_name="Hashes",
        help_text="A representation of a cryptographic digest generated over a resource using a specified hash algorithm."
        )

    def to_html(self):
        if self.href is not None:
            return self.href.first().to_html()
        else:
            return str(self.uuid)


class base64(PrimitiveModel):
    """
    base64 encoded objects such as files
    """

    class Meta:
        verbose_name = "Attachment (base64)"
        verbose_name_plural = "Attachments (base64)"

    filename = ShortTextField(
        verbose_name="File Name",
        help_text="Name of the file before it was encoded as Base64 to be embedded in a resource. This is the name that will be assigned to the file when the file is decoded."
        )
    media_type = ShortTextField(
        verbose_name="Media Type",
        help_text="Specifies a media type as defined by the Internet Assigned Numbers Authority (IANA) Media Types Registry."
        )
    value = models.TextField(
        verbose_name="base64 encoded file", help_text="A string representing arbitrary Base64-encoded binary data."
        )


class resources(BasicModel):
    """
    A resource associated with content in the containing document. A resource may be directly included in the document base64 encoded or may point to one or more equivalent internet resources.
    """

    class Meta:
        verbose_name = "Resource"
        verbose_name_plural = "Resources"

    title = ShortTextField(
        verbose_name="Resource Title",
        help_text="A name given to the resource, which may be used by a tool for display and navigation."
        )
    description = models.TextField(
        verbose_name="Description", help_text="Describes how the system satisfies a set of controls."
        )
    props = propertiesField()
    document_ids = CustomManyToManyField(
        to=document_ids, verbose_name="Document Identifiers",
        help_text="A document identifier qualified by an identifier scheme. A document identifier provides a globally unique identifier for a group of documents that are to be treated as different versions of the same document."
        )
    citation = CustomManyToManyField(
        to=citations, verbose_name="Citations",
        help_text="A citation consisting of end note text and optional structured bibliographic data."
        )
    rlinks = CustomManyToManyField(
        to=rlinks, verbose_name="Resource link",
        help_text="A pointer to an external resource with an optional hash for verification and change detection. This construct is different from link, which makes no provision for a hash or formal title."
        )
    base64 = CustomManyToManyField(
        to=base64, verbose_name="Base64 encoded objects",
        help_text="A string representing arbitrary Base64-encoded binary data."
        )

    def to_html(self):
        html_str = ""
        if len(self.rlinks.all()) > 0:
            for r in self.rlinks.all():
                html_str += "<a href='" + r.href.first().href + "' target=_blank>" + self.title + "</a>"
        return html_str


class back_matter(PrimitiveModel):
    """
    Provides a collection of identified resource objects that can be referenced by a link with a rel value of 'reference' and a href value that is a fragment '#' followed by a reference to a reference identifier. Other specialized link 'rel' values also use this pattern when indicated in that context of use.
    """

    class Meta:
        verbose_name = "Back matter"
        verbose_name_plural = "Back matter"

    resources = CustomManyToManyField(
        to=resources, verbose_name="Resources",
        help_text="A resource associated with content in the containing document. A resource may be directly included in the document base64 encoded or may point to one or more equivalent internet resources."
        )
