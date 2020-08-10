from django.db import models
from tinymce.models import HTMLField

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


# True lookup tables for storing select values
class status(models.Model):
    # system implementation status. Normally operational, under-development,
    # under-major-modification, disposition, and other but users can add custom options
    state = models.CharField(max_length=30)
    description = models.CharField(max_length=80)
    remarks = customTextField()

    def __str__(self):
        return self.state


class information_type(models.Model):
    """
    Management and support information and information systems impact levels
    as defined in NIST SP 800-60 APPENDIX C. Additional information types may be added
    by the user
    """
    title = models.CharField(max_length=100)
    description = customTextField()
    confidentialityImpact = models.CharField(max_length=50, choices=[(1, "High"), (2, "Moderate"), (3, "Low")])
    integrityImpact = models.CharField(max_length=50, choices=[(1, "High"), (2, "Moderate"), (3, "Low")])
    availabilityImpact = models.CharField(max_length=50, choices=[(1, "High"), (2, "Moderate"), (3, "Low")])

    def __str__(self):
        return self.title


class hashed_value(models.Model):
    """
    used to store hashed values for validation of attachments or linked files
    """
    value = customTextField()
    algorithm = models.CharField(max_length=100)

    def __str__(self):
        return self.algorithm


# These are common attributes of almost all objects
# Possible these should be polymorphic tables which would reduce
# complexity but likely have a negative impact on performance.

class element_property(models.Model):
    value = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100)
    property_id = models.CharField(max_length=25, blank=True)
    ns = models.CharField(max_length=25, blank=True)
    prop_class = models.CharField(max_length=25, blank=True)

    def __str__(self):
        return self.name + ': ' + self.value


class link(models.Model):
    text = models.CharField(max_length=100)
    href = models.CharField(max_length=100)
    requires_authentication = models.BooleanField(default=False)
    rel = models.CharField(max_length=100, blank=True)
    mediaType = models.CharField(max_length=100, blank=True)
    hash = models.ForeignKey(hashed_value, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.text


class annotation(models.Model):
    name = models.CharField(max_length=100)
    annotationID = models.CharField(max_length=25)
    ns = models.CharField(max_length=100)
    value = customTextField()
    remarks = customTextField()

    def __str__(self):
        return self.name


# Other common objects used in many places
class attachment(models.Model):
    attachment_type = models.CharField(max_length=50, choices=attachment_types)
    attachment = models.FileField()
    attachment_title = models.CharField(max_length=100)
    filename = models.CharField(max_length=100, blank=True)
    mediaType = models.CharField(max_length=100, blank=True)
    description = customTextField()
    hash = models.ForeignKey(hashed_value, on_delete=models.PROTECT, null=True)
    properties = customMany2ManyField(element_property)
    annotations = customMany2ManyField(annotation)
    links = customMany2ManyField(link)
    caption = models.CharField(max_length=200, blank=True)
    remarks = customTextField()

    def __str__(self):
        return self.attachment_title


# elements of a user, role, and group
class user_function(models.Model):  # list of functions assigned to roles. e.g. backup servers, deploy software, etc.
    title = models.CharField(max_length=100)
    description = customTextField()

    def __str__(self):
        return self.title


class user_privilege(models.Model):
    title = models.CharField(max_length=100)
    description = customTextField()
    functionsPerformed = customMany2ManyField(user_function)

    def __str__(self):
        return self.title


class user_role(models.Model):
    title = models.CharField(max_length=100, unique=True)
    shortName = models.CharField(max_length=25)
    desc = models.CharField(max_length=100)
    user_privileges = customMany2ManyField(user_privilege)
    properties = customMany2ManyField(element_property)
    annotations = customMany2ManyField(annotation)
    links = customMany2ManyField(link)
    remarks = customTextField()

    def __str__(self):
        return self.title


# elements that can apply to a user, organization or both
class address(models.Model):
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    postal_address = customTextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    postal_code = models.CharField(max_length=25)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class email(models.Model):
    email = models.EmailField()
    type = models.CharField(max_length=50, choices=contactInfoType, default='work')

    def __str__(self):
        return self.type + ': ' + self.email


class telephone_number(models.Model):
    number = models.CharField(max_length=25)
    type = models.CharField(max_length=25)

    def __str__(self):
        r = self.type + ': ' + self.number
        return r


class location(models.Model):
    locationID = models.CharField(verbose_name='location description', max_length=25)
    address = models.ForeignKey(address, on_delete=models.PROTECT)
    emailAddresses = customMany2ManyField(email)
    telephoneNumbers = customMany2ManyField(telephone_number)
    properties = customMany2ManyField(element_property)
    annotations = customMany2ManyField(annotation)
    links = customMany2ManyField(link)
    remarks = customTextField()

    def __str__(self):
        return self.locationID


class organization(models.Model):
    """
    Groups of people
    """
    organization_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=25)
    locations = customMany2ManyField(location)
    email_addresses = customMany2ManyField(email)
    telephone_numbers = customMany2ManyField(telephone_number)
    properties = customMany2ManyField(element_property)
    annotations = customMany2ManyField(annotation)
    links = customMany2ManyField(link)
    remarks = customTextField()

    def __str__(self):
        return self.organization_name


class person(models.Model):
    """
    An individual who can be assigned roles within a system.
    """
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=25)
    organizations = customMany2ManyField(organization)
    locations = customMany2ManyField(location)
    email_addresses = customMany2ManyField(email)
    telephone_numbers = customMany2ManyField(telephone_number)
    links = customMany2ManyField(link)
    properties = customMany2ManyField(element_property)
    annotations = customMany2ManyField(annotation)
    remarks = customTextField()

    def __str__(self):
        return self.name


class leveraged_authorization(models.Model):
    leveraged_system_name = models.CharField(max_length=255)
    link_to_SSP = models.ForeignKey(link, on_delete=models.PROTECT)

    def __str__(self):
        return self.leveraged_system_name


# System Properties

information_type_level_choices = [('high', 'High'), ('moderate', 'Moderate'), ('low', 'Low')]

class system_information_type(models.Model):
    information_type = models.ForeignKey(information_type, on_delete=models.PROTECT)
    system_information_type_name = models.CharField(max_length=255, blank=True)
    adjusted_confidentiality_impact = models.CharField(max_length=10, choices=information_type_level_choices, blank=True)
    adjusted_integrity_impact = models.CharField(max_length=10, choices=information_type_level_choices, blank=True)
    adjusted_availability_impact = models.CharField(max_length=10, choices=information_type_level_choices, blank=True)
    adjusted_confidentiality_impact_justification = customTextField()
    adjusted_integrity_impact_justification = customTextField()
    adjusted_availability_impact_justification = customTextField()

    def __str__(self):
        return self.system_information_type_name


class system_characteristic(models.Model):
    """
    required elements of a System Security Plan
    """
    system_name = models.CharField(max_length=100)
    system_short_name = models.CharField(max_length=25)
    system_description = customTextField()
    properties = customMany2ManyField(element_property)
    annotations = customMany2ManyField(annotation)
    links = customMany2ManyField(link)
    date_authorized = models.DateTimeField(null=True)
    security_sensitivity_level = models.CharField(max_length=10, choices=information_type_level_choices, blank=True)
    system_information = customMany2ManyField(system_information_type)
    security_objective_confidentiality = models.CharField(max_length=10, choices=information_type_level_choices, blank=True)
    security_objective_integrity = models.CharField(max_length=10, choices=information_type_level_choices, blank=True)
    security_objective_availability = models.CharField(max_length=10, choices=information_type_level_choices, blank=True)
    system_status = models.ForeignKey(status, on_delete=models.PROTECT, null=True)
    remarks = customTextField()
    leveraged_authorizations = customMany2ManyField(leveraged_authorization)
    authorization_boundary_diagram = models.ForeignKey(attachment, on_delete=models.PROTECT,
                                                       related_name='authorization_boundary_diagram', null=True)
    network_architecture_diagram = models.ForeignKey(attachment, on_delete=models.PROTECT,
                                                     related_name='network_architecture_diagram', null=True)
    data_flow_diagram = models.ForeignKey(attachment, on_delete=models.PROTECT, related_name='data_flow_diagram',
                                          null=True)

    def __str__(self):
        return self.system_name


class system_component(models.Model):
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
    properties = customMany2ManyField(element_property)
    annotations = customMany2ManyField(annotation)
    links = customMany2ManyField(link)
    remarks = customTextField()

    def __str__(self):
        return self.component_title


class port_range(models.Model):
    start = models.IntegerField()
    end = models.IntegerField()
    transport = models.CharField(max_length=40)

    def __str__(self):
        r = str(self.start) + '-' + str(self.end) + ' ' + self.transport
        return r


class protocol(models.Model):
    protocol_id = models.CharField(max_length=25)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    portRanges = customMany2ManyField(port_range)

    def __str__(self):
        return self.name


class system_service(models.Model):
    """
    A service is a capability offered by the information system. Examples of services include
    database access, apis, or authentication. Services are typically accessed by other systems or
    system components. System services should not to be confused with system functions which
    are typically accessed by users.
    """
    service_id = models.CharField(max_length=100)
    service_title = models.CharField(max_length=100)
    service_description = models.CharField(max_length=100)
    protocols = customMany2ManyField(protocol)
    service_purpose = customTextField()
    service_information_types = customMany2ManyField(system_information_type)
    properties = customMany2ManyField(element_property)
    annotations = customMany2ManyField(annotation)
    links = customMany2ManyField(link)
    remarks = customTextField()

    def __str__(self):
        return self.service_title


class system_interconnection(models.Model):
    system_interconnection_id = models.CharField(max_length=25)
    remote_system_name = models.CharField(max_length=100)
    interconnection_responsible_roles = customMany2ManyField(user_role)
    properties = customMany2ManyField(element_property)
    annotations = customMany2ManyField(annotation)
    links = customMany2ManyField(link)
    remarks = customTextField()

    def __str__(self):
        return self.remote_system_name


class inventory_item_type(models.Model):
    """
    generic role of an inventory item. For example, webserver, database server, network switch, edge router.
    All inventory items should be classified into an inventory item type
    """
    inventory_item_type_name = models.CharField(max_length=100)
    use = customTextField()
    description = customTextField()
    responsibleRoles = customMany2ManyField(user_role)
    baseline_configuration = models.ForeignKey(link, on_delete=models.PROTECT, blank=True,
                                               related_name='baseline_configuration')
    properties = customMany2ManyField(element_property)
    annotations = customMany2ManyField(annotation)
    links = customMany2ManyField(link)
    remarks = customTextField()


class system_inventory_item(models.Model):
    """
    Physical (or virtual) items which make up the information system.
    """
    item_id = models.CharField(max_length=100)
    inventory_item_type = models.ForeignKey(inventory_item_type, on_delete=models.PROTECT)
    item_description = customTextField()
    item_special_configuration_settings = customTextField()
    properties = customMany2ManyField(element_property)
    annotations = customMany2ManyField(annotation)
    links = customMany2ManyField(link)
    remarks = customTextField()

    def __str__(self):
        return self.item_id


# objects related to security controls

# Objects to hold control catalog data that should be displayed in the SSP

parameter_type_choices = [('label', 'Label'),
                          ('description', 'Description'),
                          ('constraint', 'Constraint'),
                          ('guidance', 'Guidance'),
                          ('value', 'Value'),
                          ('select', 'Select')]


class nist_control_parameter(models.Model):
    param_id = models.CharField(max_length=25)
    param_type = models.CharField(max_length=100, choices=parameter_type_choices)
    param_text = models.CharField(max_length=100, blank=True)
    param_depends_on = models.CharField(max_length=100, blank=True)
    param_class = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.param_id


class nist_control_statement(models.Model):
    control_id = models.CharField(max_length=7)
    statement_type = models.CharField(max_length=100)
    statement_text = customTextField()

    def __str__(self):
        return self.control_id + ' - ' + self.statement_type.capitalize()


class nist_control(models.Model):
    group_id = models.CharField(max_length=2)
    group_title = models.CharField(max_length=50)
    control_id = models.CharField(max_length=7, unique=True)
    source = models.CharField(max_length=30)
    control_title = models.CharField(max_length=255)
    parameters = customMany2ManyField(nist_control_parameter)
    label = models.CharField(max_length=10, unique=True)
    sort_id = models.CharField(max_length=10)
    status = models.CharField(max_length=30, blank=True)
    links = customMany2ManyField(link)
    control_statements = customMany2ManyField(nist_control_statement)

    def getStatementText(self, statement_type):
        t = nist_control_statement.objects.filter(control_id=self.control_id,
                                                  statement_type=statement_type).get().statement_text
        return t

    @property
    def get_guidance(self):
        return self.getStatementText('guidance')

    @property
    def get_statement(self):
        return self.getStatementText('statement')

    def __str__(self):
        long_title = self.group_title + ' | ' + self.label + ' | ' + self.control_title
        return long_title


class control_statement(models.Model):
    """
    responses to the requirements defined in each control.  control_statement_id should be
    in the format {control_id}_{requirement_id}.
    """
    control_statement_id = models.CharField(max_length=25)
    control_statement_responsible_roles = customMany2ManyField(user_role)
    control_statement_text = customTextField()
    properties = customMany2ManyField(element_property)
    links = customMany2ManyField(link)
    annotations = customMany2ManyField(annotation)
    remarks = customTextField()

    def __str__(self):
        return self.control_statement_id + ': ' + self.control_statement_text


class control_parameter(models.Model):
    control_parameter_id = models.CharField(max_length=25)
    value = customTextField()

    def __str__(self):
        return self.control_parameter_id


control_implementation_status_choices = [
    ('Implemented', 'Implemented'),
    ('Partially implemented ', 'Partially implemented'),
    ('Planned ', 'Planned'),
    ('Alternative Implementation', 'Alternative Implementation'),
    ('Not applicable', 'Not applicable')]

control_origination_choices = [
    ('Service Provider Corporate ', 'Service Provider Corporate'),
    ('Service Provider System Specific ', 'Service Provider System Specific'),
    ('Service Provider Hybrid (Corporate and System Specific)', 'Service Provider Hybrid'),
    ('Configured by Customer (Customer System Specific) ', 'Configured by Customer'),
    ('Provided by Customer (Customer System Specific) ', 'Provided by Customer'),
    ('Shared (Service Provider and Customer Responsibility) ', 'Shared'),
    ('Inherited ', 'Inherited')]


class system_control(models.Model):
    control_id = models.CharField(max_length=25)
    control_responsible_roles = customMany2ManyField(user_role)
    control_parameters = customMany2ManyField(control_parameter)
    control_statements = customMany2ManyField(control_statement)
    control_status = models.CharField(max_length=100, choices=control_implementation_status_choices)
    control_origination = models.CharField(max_length=100, choices=control_origination_choices)
    nist_control = models.ForeignKey(nist_control, on_delete=models.DO_NOTHING, null=True)
    properties = customMany2ManyField(element_property)
    annotations = customMany2ManyField(annotation)
    links = customMany2ManyField(link)
    remarks = customTextField()

    def _get_roles_list(self):
        # TODO: Figure out why this method always returns empty
        roleList = []
        for item in self.control_responsible_roles.values_list('title'):
            roleList.append(item[0])
        return roleList

    roles_list = element_property(_get_roles_list)

    def __str__(self):
        return self.control_id


class system_control_group(models.Model):
    name = models.CharField(max_length=100)
    controls = customMany2ManyField(system_control)


class system_user(models.Model):
    user = models.ForeignKey(person,on_delete=models.PROTECT)
    roles = customMany2ManyField(user_role)


class system_security_plan(models.Model):
    sspID = models.CharField(max_length=25)
    title = models.CharField(max_length=100)
    published = models.DateTimeField()
    lastModified = models.DateTimeField()
    version = models.CharField(max_length=25, default='1.0.0')
    oscalVersion = models.CharField(max_length=10, default='1.0.0')
    system_characteristics = models.ForeignKey(system_characteristic, on_delete=models.PROTECT)
    system_components = customMany2ManyField(system_component)
    system_services = customMany2ManyField(system_service)
    system_interconnections = customMany2ManyField(system_interconnection)
    system_inventory_items = customMany2ManyField(system_inventory_item)
    controls = customMany2ManyField(system_control)
    control_groups = customMany2ManyField(system_control_group)
    properties = customMany2ManyField(element_property)
    links = customMany2ManyField(link)
    system_users = customMany2ManyField(system_user)
    remarks = customTextField()

    def __str__(self):
        return self.title
