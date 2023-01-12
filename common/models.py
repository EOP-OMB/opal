import logging
import os.path
import base64 as base64_encoder
from urllib.parse import urlencode

from django.db import models, IntegrityError, connection, OperationalError
from django.core.validators import RegexValidator
import uuid
from itertools import chain
from django.conf import settings
from django.utils.timezone import now

import catalog
from common.functions import replace_hyphen, search_for_uuid
from django.core.exceptions import ObjectDoesNotExist  # ValidationError
from django.urls import reverse
from ckeditor.fields import RichTextField
import json


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
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['blank']
        return name, path, args, kwargs

    def first(self):
        pass


class properties_field(CustomManyToManyField):
    def __init__(self, *args, **kwargs):
        kwargs['to'] = "common.props"
        kwargs['verbose_name'] = "Properties"
        kwargs[
            'help_text'] = "An attribute, characteristic, or quality of the containing object expressed as a namespace qualified name/value pair. The value of a property is a simple scalar value, which may be expressed as a list of values."
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
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
    ("alternative",
     "Alternative: There is an alternative implementation for this control as explained in the remarks.",),
    ("not-applicable", "Not-Applicable: This control does not apply to this system as justified in the remarks.",)
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

    def get_create_url(self):
        admin_str = 'admin:' + "_".join([self._meta.app_label, self._meta.model_name, 'add'])
        change_url = reverse(admin_str)
        return change_url

    def to_dict(self):
        opts = self._meta
        excluded_fields = ['id', 'pk', 'created_at', 'updated_at']
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
        data = self.convert_field_names_from_db_to_oscal(data)
        return data

    def to_json(self):
        data = self.to_dict()
        return json.dumps(data, indent=2)


    def to_html(self, indent=0):
        opts = self._meta
        # list of some excluded fields
        excluded_fields = ['id', 'pk', 'created_at', 'updated_at', 'uuid']

        html_str = "\n<div style='margin-left: " + str(indent * 20) + "px;'>"
        # getting all fields that available in `Client` model,
        # but not in `excluded_fields`
        for f in opts.concrete_fields:
            if f.name not in excluded_fields:
                if f.get_internal_type() == 'ForeignKey':
                    child = self.__getattribute__(f.name)
                    if child is not None:
                        value = child.to_html(indent=indent + 1)
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
                html_str += "<li>" + f.verbose_name + " <a href='" + self.get_create_url() + "'>(Add)</a>:</li>\n"
                new_indent = indent + 1
                for i in f.value_from_object(self):
                    html_str += i.to_html(indent=new_indent)
        html_str += "</ul>\n</div>"
        if html_str is None:
            html_str = "None"
        return html_str

    def field_name_changes(self):
        """returns a dictionary of fileds that are named differntly in the model than in OSCAL JSON. The format is {oscal_filed_name: database_field_name}"""
        return {}

    def convert_field_names_from_db_to_oscal(self, d):
        new_dict = {}
        del_keys = set()
        if type(d) is dict:
            if len(self.field_name_changes()) == 0:
                # No specific field list, just fix the hyphens
                for k in d:
                    if "_" in k:
                        new_key = k.replace("_", "-")
                        new_dict[new_key] = d[k]
                        del_keys.add(k)
            else:
                # if object has a custom list it will include any hyphens
                name_change_list: dict = self.field_name_changes()
                reverse_name_change_list = {}
                for k in name_change_list:
                    reverse_name_change_list[name_change_list[k]] = k
                if type(name_change_list) is dict:
                    for k in d:
                        if k in reverse_name_change_list:
                            new_key = reverse_name_change_list[k]
                            new_dict[new_key] = d[k]
                            del_keys.add(k)
            for k in del_keys:
                d.pop(k)
            merged_dict = {**new_dict, **d}
        else:
            merged_dict = d
        return merged_dict

    def convert_field_names_from_oscal_to_db(self, d):
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

    def unique_field_list(self):
        field_list = []
        for f in self._meta.concrete_fields:
            if f.name not in ['created_at', 'updated_at', 'id', 'uuid']:
                if not f.null and not f.is_relation:
                    field_list.append(f.name)
        if len(field_list) == 0:
            field_list.append('uuid')
        return field_list

    # def import_oscal(self, oscal_data):
    #     logger = logging.getLogger("django")
    #     opts = self._meta
    #     self = self.check_for_existing_object()
    #     logger.info("Starting import for " + opts.model_name)
    #     if oscal_data is None or len(oscal_data) == 0:
    #         logger.warning("oscal_data is 0 length")
    #     excluded_fields = ['id', 'pk', 'created_at', 'updated_at']
    #     field_list = list(opts.concrete_fields)
    #     field_list_str = []
    #     logger.debug("Removing excluded fields from field_list")
    #     for f in field_list:
    #         if f.name in excluded_fields:
    #             field_list.remove(f)
    #         else:
    #             field_list_str.append(f.name)
    #     logger.debug("model = " + opts.model_name)
    #     logger.debug("field_list = " + ', '.join(field_list_str))
    #     if type(oscal_data) is dict:
    #         logger.debug("Handling dictionary...")
    #         # replace field names to match internal model names
    #         oscal_data = self.convert_field_names_from_oscal_to_db(oscal_data)
    #         for f in field_list:
    #             if f.name in oscal_data.keys():
    #                 if f.get_internal_type() == 'ForeignKey':
    #                     logger.debug(f.name + " is a foreign key. Creating child object...")
    #                     child = f.related_model()
    #                     child = child.import_oscal(oscal_data[f.name])
    #                     self.__setattr__(f.name, child)
    #                     logger.debug("Created new " + f.name + " with id " + str(child.id))
    #                 else:
    #                     field = f.name
    #                     value = oscal_data[f.name]
    #                     if type(value) is str:
    #                         logger.debug("Setting " + field + " to " + value)
    #                         self.__setattr__(field, value)
    #                     else:
    #                         logger.warning(field + " value is a " + str(type(value)))
    #                     logger.debug("Done")
    #     elif type(oscal_data) is str:
    #         logger.debug("Handling string...")
    #         # maybe the model has just one field?
    #         if 'uuid' in field_list:
    #             copy_field_list = field_list.copy()
    #             copy_field_list.remove('uuid')
    #             if len(copy_field_list) == 1:
    #                 field = field_list[0]
    #                 value = oscal_data
    #                 self.__setattr__(field, value)
    #             else:
    #                 uuid_obj = False
    #                 try:
    #                     uuid_obj = uuid.UUID(oscal_data, version=4)
    #                 except ValueError:
    #                     logger.error(oscal_data + " is not a valid uuid")
    #                 if uuid_obj:
    #                     self = self.check_for_existing_object({'uuid': uuid_obj})
    #                     field = 'uuid'
    #                     value = uuid_obj
    #                     self.__setattr__(field, value)
    #         else:
    #             logger.error("oscal_data does not provide a field name. " + opts.model_name + " with oscal_data " + oscal_data)
    #     else:
    #         logger.error("oscal_data is not a dictionary, string, or list.  oscal_data:")
    #         logger.error(oscal_data)
    #     self.save()
    #     logger.debug('Handling the many_to_many fields')
    #     field_list = list(opts.many_to_many)
    #     logger.debug("field_list = " + ', '.join(field_list_str))
    #     if type(oscal_data) is dict:
    #         for f in field_list:
    #             if f.name in oscal_data.keys():
    #                 if type(oscal_data[f.name]) is dict and len(oscal_data) > 0:
    #                     logger.debug("Creating child object for field " + f.name)
    #                     child = f.related_model()
    #                     child = child.import_oscal(oscal_data[f.name])
    #                     self.oscal_import_save_m2m(child, f, opts)
    #                 elif type(oscal_data[f.name]) is list and len(oscal_data[f.name]) > 0:
    #                     for item in oscal_data[f.name]:
    #                         logger.debug("Creating child object for field " + f.name)
    #                         child = f.related_model()
    #                         child = child.import_oscal(item)
    #                         self.oscal_import_save_m2m(child, f, opts)
    #                 elif type(oscal_data[f.name]) is str:
    #                     logger.debug("Creating child object for field " + f.name)
    #                     child = f.related_model()
    #                     child = child.import_oscal(oscal_data)
    #                     self.oscal_import_save_m2m(child, f, opts)
    #                 else:
    #                     child = None
    #                 self.save()
    #             elif type(oscal_data) is str:
    #                 logger.debug("Creating child object for field " + f.name)
    #                 field = f.name
    #                 value = oscal_data
    #                 self.__setattr__(field, value)
    #                 self.save()
    #     self.save()
    #     logger.info("Completed import for " + opts.model_name)
    #     return self

    def excluded_fields(self):
        """returns a list of fields to ignore durring import and other functions"""
        return ['id', 'pk', 'created_at', 'updated_at']

    def import_oscal(self, oscal_data):
        logger = logging.getLogger("django")
        opts = self._meta
        logger.info("Starting import for " + opts.model_name)
        if oscal_data is None or len(oscal_data) == 0:
            logger.warning("oscal_data is 0 length")
            return None
        # replace field names to match internal model names
        oscal_data = self.convert_field_names_from_oscal_to_db(oscal_data)
        existing_object = self.check_for_existing_object(oscal_data)
        if existing_object != self:
            return existing_object
        excluded_fields = self.excluded_fields
        field_list = list(opts.concrete_fields)
        field_list_str = []
        logger.debug("Removing excluded fields from field_list")
        for f in field_list:
            if f.name in excluded_fields():
                field_list.remove(f)
            else:
                field_list_str.append(f.name)
        logger.debug("model = " + opts.model_name)
        logger.debug("field_list = " + ', '.join(field_list_str))
        if type(oscal_data) is dict:
            logger.debug("Handling dictionary...")
            for f in field_list:
                if f.name in oscal_data.keys():
                    if f.get_internal_type() == 'ForeignKey':
                        logger.debug(f.name + " is a foreign key. Creating child object...")
                        child = f.related_model()
                        child = child.import_oscal(oscal_data[f.name])
                        self.__setattr__(f.name, child)
                        logger.debug("Created new " + f.name + " with id " + str(child.id))
                    else:
                        field = f.name
                        value = oscal_data[f.name]
                        if type(value) is str:
                            logger.debug("Setting " + field + " to " + value)
                            self.__setattr__(field, value)
                        else:
                            logger.warning(field + " value is a " + str(type(value)))
                        logger.debug("Done")
        elif type(oscal_data) is str:
            logger.debug("Handling string...")
            # maybe the model has just one field?
            if 'uuid' in field_list:
                copy_field_list = field_list.copy()
                copy_field_list.remove('uuid')
                if len(copy_field_list) == 1:
                    field = field_list[0]
                    value = oscal_data
                    self.__setattr__(field, value)
                else:
                    uuid_obj = False
                    try:
                        uuid_obj = uuid.UUID(oscal_data, version=4)
                    except ValueError:
                        logger.error(oscal_data + " is not a valid uuid")
                    if uuid_obj:
                        self = self.check_for_existing_object({'uuid': uuid_obj})
                        field = 'uuid'
                        value = uuid_obj
                        self.__setattr__(field, value)
            else:
                logger.error(
                    "oscal_data does not provide a field name. " + opts.model_name + " with oscal_data " + oscal_data)
        else:
            logger.error("oscal_data is not a dictionary, string, or list.  oscal_data:")
            logger.error(oscal_data)
        self.save()
        logger.debug('Handling the many_to_many fields')
        field_list = list(opts.many_to_many)
        logger.debug("field_list = " + ', '.join(field_list_str))
        if type(oscal_data) is dict:
            for f in field_list:
                if f.name in oscal_data.keys():
                    if type(oscal_data[f.name]) is dict and len(oscal_data) > 0:
                        logger.debug("Creating child object for field " + f.name)
                        child = f.related_model()
                        child = child.import_oscal(oscal_data[f.name])
                        self.add_m2m(child, f, opts)
                        self.save()
                    elif type(oscal_data[f.name]) is list and len(oscal_data[f.name]) > 0:
                        for item in oscal_data[f.name]:
                            logger.debug("Creating child object for field " + f.name)
                            child = f.related_model()
                            child = child.import_oscal(item)
                            self.add_m2m(child, f, opts)
                            self.save()
                    elif type(oscal_data[f.name]) is str:
                        logger.debug("Creating child object for field " + f.name)
                        child = f.related_model()
                        child = child.import_oscal(oscal_data)
                        self.add_m2m(child, f, opts)
                        self.save()
                    else:
                        child = None
                    self.save()
                elif type(oscal_data) is str:
                    logger.debug("Creating child object for field " + f.name)
                    field = f.name
                    value = oscal_data
                    self.__setattr__(field, value)
                    self.save()
        self.save()
        logger.info("Completed import for " + opts.model_name)
        return self

    def check_for_existing_object(self, oscal_data):
        """
        Checks for an existing object. values_dict is a key:value list of fields to check.
        """
        logger = logging.getLogger('django')
        unique_field_dict = {}
        for f in self.unique_field_list():
            if f in oscal_data.keys():
                unique_field_dict[f] = oscal_data[f]
        logger.info("Checking for an existing %s with fields matching %s" % (self._meta.model_name, unique_field_dict))
        if self._meta.model.objects.filter(**unique_field_dict).exists():
            logger.info("Found an existing %s with fields matching %s" % (self._meta.model_name, unique_field_dict))
            existing_object = self._meta.model.objects.filter(**unique_field_dict).first()
            return existing_object
        else:
            logger.info(
                "Could not find an existing %s with fields matching %s" % (self._meta.model_name, unique_field_dict))
            return self

    def add_m2m(self, child, f, opts):
        logger = logging.getLogger("django")
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
                logger.error("Relationship already exists. sql = " + sql)
            except OperationalError as err:
                logger.error("An error occurred")
                logger.error(err)

    # def oscal_import_save_m2m(self, child, f, opts):
    #     logger = logging.getLogger("django")
    #     if child is not None:
    #         error = False
    #         try:
    #             child.save()
    #         except IntegrityError:
    #             try:
    #                 existing_child = child._meta.model.objects.get(uuid=child.uuid)
    #                 child = existing_child
    #             except ObjectDoesNotExist:
    #                 logger.error("Integrity error occurred but no matching object found with the same uuid")
    #                 error = True
    #         if self.id is None:
    #             logger.error("Parent id is None")
    #             try:
    #                 self.save()
    #             except IntegrityError as err:
    #                 logger.error(err)
    #                 error = True
    #         if child.id is None:
    #             logger.error("Child id is none")
    #             try:
    #                 child.save()
    #             except IntegrityError as err:
    #                 logger.error(err)
    #                 error = True
    #         if not error:
    #             parent_id = self.id
    #             parent_field_name = opts.model_name + "_id"
    #             child_id = child.id
    #             child_field_name = child._meta.model_name + "_id"
    #             if parent_field_name == child_field_name:
    #                 child_field_name = "to_" + child_field_name
    #                 parent_field_name = "from_" + parent_field_name
    #             table_name = f.m2m_db_table()
    #             sql = "INSERT INTO " + table_name + " (" + parent_field_name + "," + child_field_name + ") VALUES(" + str(
    #                 parent_id
    #                 ) + "," + str(child_id) + ")"
    #             with connection.cursor() as cursor:
    #                 try:
    #                     cursor.execute(sql)
    #                 except IntegrityError:
    #                     logger.error("Relationship already exists. sql = " + sql)
    #                 except OperationalError as err:
    #                     logger.error("An error occurred")
    #                     logger.error(err)
    #     return child

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
    remarks = RichTextField(
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


link_rel_options = [
    ("related", "related"),
    ("moved-to", "moved-to"),
    ("canonical", "canonical"),
    ("incorporated-into", "incorporated-into"),
    ("required", "required"),
    ("reference", "reference"),
    ("alternate", "alternate"),
]


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
        blank=True, choices=link_rel_options
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

    def to_html(self, indent=0):
        href = ''
        href_text = ''
        if len(self.href) > 0:
            if self.rel in ['related', 'moved-to', 'incorporated-into', 'required']:
                # link should be to another control in the same catalog
                if catalog.models.controls.objects.filter(control_id=self.href[1:]).count() == 1:
                    href = catalog.models.controls.objects.get(control_id=self.href[1:]).get_absolute_url()
                    href_text = catalog.models.controls.objects.get(control_id=self.href[1:]).__str__()
                    html_str = "<a href='" + href + "' target=_blank>" + href_text + "</a>"
                else:
                    html_str = "<--There is a broken link in the database. Link id %s is a related link but no control with id %s can be found-->" % (
                    self.id, self.href[1:])
            if self.rel in ['canonical', 'reference', 'alternate']:
                if resources.objects.filter(uuid=self.href[1:]).count() == 1:
                    # href = "https://www.google.com/search?q=%s" % urlencode(resources.objects.get(uuid=self.href[1:]).title)
                    href = ""
                    href_text = resources.objects.get(uuid=self.href[1:]).title
                    html_str = href_text + "<br>"
                else:
                    html_str = "<!-- Could not find an object matching uuid " + self.href[1:] + " in the database -->"
        else:
            html_str = "<--There is a broken link in the database. Link id %s has no href value-->" % self.id
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
    props = properties_field()


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
    description = RichTextField(
        verbose_name="Role Description", help_text="A summary of the role's purpose and associated responsibilities.",
        blank=True
    )
    props = properties_field()
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
    props = properties_field()
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
    props = properties_field()
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
    props = properties_field()
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
    props = properties_field()
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


    def __str__(self):
        return self.title


class citations(PrimitiveModel):
    """
    A citation consisting of end note text and optional structured bibliographic data.
    """

    class Meta:
        verbose_name = "Citation"
        verbose_name_plural = "Citations"

    text = ShortTextField(verbose_name="Citation Text", help_text="A line of citation text.")
    props = properties_field()
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

    def to_html(self, indent=0):
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

    def render_file(self):
        binary_file = bytes(self.value, encoding='utf-8')
        return base64_encoder.decodebytes(binary_file)

    def get_absolute_url(self):
        return reverse('common:base64_detail', args=(self.pk,))

    def __str__(self):
        return "%s (%s)" % (self.filename, self.media_type,)


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
    description = RichTextField(
        verbose_name="Description", help_text="Describes how the system satisfies a set of controls."
    )
    props = properties_field()
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

    def to_html(self, indent=0):
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
