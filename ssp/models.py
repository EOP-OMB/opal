from django.db import models
from tinymce.models import HTMLField
import uuid

# TODO create a json function for each class


contactInfoType = [('work', 'Work'),
                   ('personal', 'Personal'),
                   ('shared', 'Shared'),
                   ('service', 'Service'),
                   ('other', 'Other')]

attachment_types = [('image', 'Image'),
                    ('diagram', 'Diagram'),
                    ('document', 'Document'),
                    ('other', 'Other File Type')]


# Define some common field types

class customMany2ManyField(models.ManyToManyField):
    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)


class customTextField(HTMLField):
    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['blank']
        return name, path, args, kwargs


class PrimitiveModel(models.Model):
    uuid = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)

    class Meta:
        abstract = True

    def natural_key(self):
        return self.uuid


class BasicModel(PrimitiveModel):
    title = models.CharField(max_length=255, blank=True, help_text='A title for display and navigation')
    short_name = models.CharField(max_length=255, blank=True, help_text='A common name, short name, or acronym')
    desc = customTextField('description', help_text='A short textual description')
    remarks = customTextField(help_text='general notes or comments')

    class Meta:
        abstract = True
        ordering = ["title"]

    def __str__(self):
        return self.title + ' (' + self.short_name + ')'


# True lookup tables for storing select values
class status(BasicModel):
    # system implementation status. Normally operational, under-development,
    # under-major-modification, disposition, and other but users can add custom options
    state = models.CharField(max_length=30)


class information_type(BasicModel):
    """
    Management and support information and information systems impact levels
    as defined in NIST SP 800-60 APPENDIX C. Additional information types may be added
    by the user
    """
    confidentialityImpact = models.CharField(max_length=50, choices=[(1, "High"), (2, "Moderate"), (3, "Low")])
    integrityImpact = models.CharField(max_length=50, choices=[(1, "High"), (2, "Moderate"), (3, "Low")])
    availabilityImpact = models.CharField(max_length=50, choices=[(1, "High"), (2, "Moderate"), (3, "Low")])


class hashed_value(BasicModel):
    """
    used to store hashed values for validation of attachments or linked files
    """
    value = customTextField()
    algorithm = models.CharField(max_length=100)


# These are common attributes of almost all objects
# Possible these should be polymorphic tables which would reduce
# complexity but likely have a negative impact on performance.

class element_property(PrimitiveModel):
    value = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100)
    property_id = models.CharField(max_length=25, blank=True)
    ns = models.CharField(max_length=25, blank=True)
    prop_class = models.CharField(max_length=25, blank=True)

    def __str__(self):
        return self.name + ': ' + self.value


class link(PrimitiveModel):
    text = models.CharField(max_length=255)
    href = models.CharField(max_length=255)
    requires_authentication = models.BooleanField(default=False)
    rel = models.CharField(max_length=255, blank=True)
    mediaType = models.CharField(max_length=255, blank=True)
    hash = models.ForeignKey(hashed_value, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.text


class annotation(BasicModel):
    annotationID = models.CharField(max_length=25)
    ns = models.CharField(max_length=100)
    value = customTextField()


class ExtendedBasicModel(BasicModel):
    """
    Basic fields plus properties, annotations, and links
    """
    properties = customMany2ManyField(element_property)
    annotations = customMany2ManyField(annotation)
    links = customMany2ManyField(link)

    class Meta:
        abstract = True


# Other common objects used in many places
class attachment(ExtendedBasicModel):
    attachment_type = models.CharField(max_length=50, choices=attachment_types)
    attachment = models.FileField()
    filename = models.CharField(max_length=100, blank=True)
    mediaType = models.CharField(max_length=100, blank=True)
    hash = models.ForeignKey(hashed_value, on_delete=models.PROTECT, null=True)
    caption = models.CharField(max_length=200, blank=True)


# elements of a user, role, and group
class user_function(BasicModel):
    """
    list of functions assigned to roles. e.g. backup servers, deploy software, etc.
    """


class user_privilege(BasicModel):
    functionsPerformed = customMany2ManyField(user_function)


class user_role(ExtendedBasicModel):
    user_privileges = customMany2ManyField(user_privilege)


# elements that can apply to a user, organization or both
class address(BasicModel):
    type = models.CharField(max_length=100)
    postal_address = customTextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    postal_code = models.CharField(max_length=25)
    country = models.CharField(max_length=100)


class email(PrimitiveModel):
    email = models.EmailField()
    type = models.CharField(max_length=50, choices=contactInfoType, default='work')
    supports_rich_text = models.BooleanField(default=True)

    def __str__(self):
        return self.type + ': ' + self.email


class telephone_number(PrimitiveModel):
    number = models.CharField(max_length=25)
    type = models.CharField(max_length=25)

    def __str__(self):
        return self.type + ': ' + self.number


class location(ExtendedBasicModel):
    address = models.ForeignKey(address, on_delete=models.PROTECT)
    emailAddresses = customMany2ManyField(email)
    telephoneNumbers = customMany2ManyField(telephone_number)


class organization(ExtendedBasicModel):
    """
    Groups of people
    """
    locations = customMany2ManyField(location)
    email_addresses = customMany2ManyField(email)
    telephone_numbers = customMany2ManyField(telephone_number)


class person(ExtendedBasicModel):
    """
    An individual who can be assigned roles within a system.
    """
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=25)
    organizations = customMany2ManyField(organization)
    locations = customMany2ManyField(location)
    email_addresses = customMany2ManyField(email)
    telephone_numbers = customMany2ManyField(telephone_number)

    def __str__(self):
        return self.name


# System Properties

information_type_level_choices = [('high', 'High'), ('moderate', 'Moderate'), ('low', 'Low')]


class system_information_type(BasicModel):
    information_type = models.ForeignKey(information_type, on_delete=models.PROTECT)
    system_information_type_name = models.CharField(max_length=255, blank=True)
    adjusted_confidentiality_impact = models.CharField(max_length=10, choices=information_type_level_choices,
                                                       blank=True)
    adjusted_integrity_impact = models.CharField(max_length=10, choices=information_type_level_choices, blank=True)
    adjusted_availability_impact = models.CharField(max_length=10, choices=information_type_level_choices, blank=True)
    adjusted_confidentiality_impact_justification = customTextField()
    adjusted_integrity_impact_justification = customTextField()
    adjusted_availability_impact_justification = customTextField()


class system_characteristic(ExtendedBasicModel):
    """
    required elements of a System Security Plan
    """
    date_authorized = models.DateTimeField(null=True)
    security_sensitivity_level = models.CharField(max_length=10, choices=information_type_level_choices, blank=True)
    system_information = customMany2ManyField(system_information_type)
    security_objective_confidentiality = models.CharField(max_length=10, choices=information_type_level_choices,
                                                          blank=True)
    security_objective_integrity = models.CharField(max_length=10, choices=information_type_level_choices, blank=True)
    security_objective_availability = models.CharField(max_length=10, choices=information_type_level_choices,
                                                       blank=True)
    system_status = models.ForeignKey(status, on_delete=models.PROTECT, null=True)
    authorization_boundary_diagram = models.ForeignKey(attachment, on_delete=models.PROTECT,
                                                       related_name='authorization_boundary_diagram', null=True)
    network_architecture_diagram = models.ForeignKey(attachment, on_delete=models.PROTECT,
                                                     related_name='network_architecture_diagram', null=True)
    data_flow_diagram = models.ForeignKey(attachment, on_delete=models.PROTECT, related_name='data_flow_diagram',
                                          null=True)


class system_component(ExtendedBasicModel):
    """
    A component is a subset of the information system that is either severable or
    should be described in additional detail. For example, this might be an authentication
    provider or a backup tool.
    """
    component_type = models.CharField(max_length=100)
    component_title = models.CharField(max_length=100)
    component_description = customTextField()
    component_information_types = customMany2ManyField(system_information_type)
    component_status = models.ForeignKey(status, on_delete=models.PROTECT, null=True)
    component_responsible_roles = customMany2ManyField(user_role)


class port_range(BasicModel):
    start = models.IntegerField()
    end = models.IntegerField()
    transport = models.CharField(max_length=40)

    def __str__(self):
        r = str(self.start) + '-' + str(self.end) + ' ' + self.transport
        return r


class protocol(BasicModel):
    portRanges = customMany2ManyField(port_range)


class system_service(ExtendedBasicModel):
    """
    A service is a capability offered by the information system. Examples of services include
    database access, apis, or authentication. Services are typically accessed by other systems or
    system components. System services should not to be confused with system functions which
    are typically accessed by users.
    """
    protocols = customMany2ManyField(protocol)
    service_purpose = customTextField()
    service_information_types = customMany2ManyField(system_information_type)


class system_interconnection(ExtendedBasicModel):
    interconnection_responsible_roles = customMany2ManyField(user_role)


class inventory_item_type(ExtendedBasicModel):
    """
    generic role of an inventory item. For example, webserver, database server, network switch, edge router.
    All inventory items should be classified into an inventory item type
    """
    use = customTextField()
    responsibleRoles = customMany2ManyField(user_role)
    baseline_configuration = models.ForeignKey(link, on_delete=models.PROTECT, blank=True,
                                               related_name='baseline_configuration')


class system_inventory_item(ExtendedBasicModel):
    """
    Physical (or virtual) items which make up the information system.
    """
    inventory_item_type = models.ForeignKey(inventory_item_type, on_delete=models.PROTECT)
    item_special_configuration_settings = customTextField()


# objects related to security controls

# Objects to hold control catalog data that should be displayed in the SSP

parameter_type_choices = [('label', 'Label'),
                          ('description', 'Description'),
                          ('constraint', 'Constraint'),
                          ('guidance', 'Guidance'),
                          ('value', 'Value'),
                          ('select', 'Select')]


class nist_control_parameter(PrimitiveModel):
    param_id = models.CharField(max_length=255)
    param_type = models.CharField(max_length=255, choices=parameter_type_choices)
    param_text = models.CharField(max_length=255, blank=True)
    param_depends_on = models.CharField(max_length=255, blank=True)
    param_class = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.param_id


class nist_control_statement(PrimitiveModel):
    # control_id = models.CharField(max_length=50)
    nist_control = models.ForeignKey('nist_control', on_delete=models.PROTECT, null=True)
    statement_type = models.CharField(max_length=255)
    statement_text = customTextField()

    def __str__(self):
        return self.nist_control.label + ' - ' + self.statement_type.capitalize()


class nist_control(PrimitiveModel):
    group_id = models.CharField(max_length=50)
    group_title = models.CharField(max_length=255)
    control_id = models.CharField(max_length=50, unique=True)
    source = models.CharField(max_length=50)
    control_title = models.CharField(max_length=255)
    parameters = customMany2ManyField(nist_control_parameter)
    label = models.CharField(max_length=50, unique=True)
    sort_id = models.CharField(max_length=50)
    status = models.CharField(max_length=255, blank=True)
    links = customMany2ManyField(link)

    # control_statements = customMany2ManyField(nist_control_statement,related_name='stmt')

    def getStatementText(self, statement_type):
        t = nist_control_statement.objects.filter(nist_control=self,
                                                  statement_type=statement_type).get().statement_text
        return t

    @property
    def get_guidance(self):
        return self.getStatementText('guidance')

    @property
    def get_statement(self):
        return self.getStatementText('statement')

    # TODO: Add methods for objectives and whatever the other type is

    # def get_control_implementation(self, info_sys):
    #     c = []
    #     ssp = system_security_plan.objects.get(pk=info_sys)
    #     nc = self
    #     if ssp.controls.filter(nist_control=nc).exists():
    #         print(nc.__str__() + ' exists for system')
    #         c.append({ssp.__str__(): ssp.controls.get(nist_control=nc)})
    #     if ssp.leveraged_authorization.exists():
    #         for leveraged_auth in ssp.leveraged_authorization.all():
    #             if leveraged_auth.controls.filter(nist_control=nc, inheritable=True).exists():
    #                 print(nc.__str__() + ' exists for leveraged system')
    #                 c.append({ssp.__str__(): ssp.controls.get(nist_control=nc)})
    #     return c

    def __str__(self):
        long_title = self.group_title + ' | ' + self.label + ' | ' + self.control_title
        return long_title


class control_statement(ExtendedBasicModel):
    """
    responses to the requirements defined in each control.  control_statement_id should be
    in the format {control_id}_{requirement_id}.
    """
    control_statement_id = models.CharField(max_length=25)
    control_statement_responsible_roles = customMany2ManyField(user_role)
    control_statement_text = customTextField()


class control_parameter(BasicModel):
    control_parameter_id = models.CharField(max_length=25)
    value = customTextField()


# class control_implementation(ExtendedBasicModel):
    # control_id = models.CharField(max_length=25)
    # control_responsible_roles = customMany2ManyField(user_role)
    # control_parameters = customMany2ManyField(control_parameter)
    # control_statements = customMany2ManyField(control_statement)
    # nist_control = models.ForeignKey(nist_control, on_delete=models.DO_NOTHING, null=True, blank=True)


control_implementation_status_choices = [
    ('Implemented', 'Implemented'),
    ('Partially Implemented ', 'Partially Implemented'),
    ('Planned ', 'Planned'),
    ('Alternative Implementation', 'Alternative Implementation'),
    ('Not Applicable', 'Not Applicable'),
    ('Other than Implemented', 'Other than Implemented')]

control_origination_choices = [
    ('Service Provider Corporate ', 'Service Provider Corporate'),
    ('Service Provider System Specific ', 'Service Provider System Specific'),
    ('Service Provider Hybrid (Corporate and System Specific)', 'Service Provider Hybrid'),
    ('Configured by Customer (Customer System Specific) ', 'Configured by Customer'),
    ('Provided by Customer (Customer System Specific) ', 'Provided by Customer'),
    ('Shared (Service Provider and Customer Responsibility) ', 'Shared'),
    ('Inherited ', 'Inherited'),
    ('N/A', 'N/A')]


class system_control(ExtendedBasicModel):
    # control_id = models.CharField(max_length=25)
    # control_implementation = models.ForeignKey(control_implementation, on_delete=models.PROTECT, null=True)
    control_responsible_roles = customMany2ManyField(user_role)
    control_parameters = customMany2ManyField(control_parameter)
    control_statements = customMany2ManyField(control_statement)
    control_status = models.CharField(max_length=100, choices=control_implementation_status_choices)
    control_origination = models.CharField(max_length=100, choices=control_origination_choices)
    nist_control = models.ForeignKey(nist_control, on_delete=models.DO_NOTHING, null=True)
    information_system = models.ForeignKey('system_security_plan', on_delete=models.PROTECT, null=True)
    inheritable = models.BooleanField(default=False)

    @property
    def sorted_statement_set(self):
        return self.control_statements.order_by('control_statement_id')

    def __str__(self):
        return self.information_system.short_name + ' | ' + self.nist_control.__str__()


class control_baseline(BasicModel):
    controls = customMany2ManyField(nist_control)


class system_user(BasicModel):
    user = models.ForeignKey(person, on_delete=models.PROTECT)
    roles = customMany2ManyField(user_role)


class system_security_plan(ExtendedBasicModel):
    published = models.DateTimeField()
    lastModified = models.DateTimeField()
    version = models.CharField(max_length=25, default='1.0.0')
    oscalVersion = models.CharField(max_length=10, default='1.0.0')
    system_characteristics = models.ForeignKey(system_characteristic, on_delete=models.PROTECT)
    system_components = customMany2ManyField(system_component)
    system_services = customMany2ManyField(system_service)
    system_interconnections = customMany2ManyField(system_interconnection)
    system_inventory_items = customMany2ManyField(system_inventory_item)
    control_baseline = models.ForeignKey(control_baseline, on_delete=models.PROTECT, null=True)
    additional_selected_controls = customMany2ManyField(nist_control)
    leveraged_authorization = customMany2ManyField('system_security_plan')
    controls = customMany2ManyField(system_control)
    system_users = customMany2ManyField(system_user)

    def _get_selected_controls(self):
        selected_controls = self.control_baseline.controls
        for item in self.additional_selected_controls.all():
            selected_controls.add(item)
        return selected_controls

    @property
    def selected_controls(self):
        return self._get_selected_controls()
