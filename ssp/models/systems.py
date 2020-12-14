from ssp.models.controls import *

# System Properties

information_type_level_choices = [('high', 'High'), ('moderate', 'Moderate'), ('low', 'Low')]


class system_component(ExtendedBasicModel):
    """
    A component is a subset of the information system that is either severable or
    should be described in additional detail. For example, this might be an authentication
    provider or a backup tool.
    """
    component_type = models.CharField(max_length=100)
    component_title = models.CharField(max_length=100)
    component_description = customTextField()
    component_information_types = customMany2ManyField(information_type)
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
    service_information_types = customMany2ManyField(information_type)


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


class system_user(BasicModel):
    user = models.ForeignKey(person, on_delete=models.PROTECT, related_name='system_user_set')
    roles = customMany2ManyField(user_role)


class system_security_plan(ExtendedBasicModel):
    published = models.DateTimeField()
    lastModified = models.DateTimeField()
    version = models.CharField(max_length=25, default='1.0.0')
    oscalVersion = models.CharField(max_length=10, default='1.0.0')
    # system_characteristics = models.ForeignKey(system_characteristic, on_delete=models.PROTECT)
    system_components = customMany2ManyField(system_component)
    system_services = customMany2ManyField(system_service)
    system_interconnections = customMany2ManyField(system_interconnection)
    system_inventory_items = customMany2ManyField(system_inventory_item)
    control_baseline = models.ForeignKey(control_baseline, on_delete=models.PROTECT, null=True)
    additional_selected_controls = customMany2ManyField(nist_control)
    leveraged_authorization = customMany2ManyField('system_security_plan')
    controls = customMany2ManyField(system_control)
    system_users = customMany2ManyField(system_user)
    date_authorized = models.DateTimeField(null=True)
    security_sensitivity_level = models.CharField(max_length=10, choices=information_type_level_choices, blank=True)
    information_types = customMany2ManyField(information_type)
    security_objective_confidentiality = models.CharField(max_length=10, choices=information_type_level_choices,
                                                          blank=True)
    security_objective_integrity = models.CharField(max_length=10, choices=information_type_level_choices, blank=True)
    security_objective_availability = models.CharField(max_length=10, choices=information_type_level_choices,
                                                       blank=True)
    system_status = models.ForeignKey(status, on_delete=models.PROTECT, null=True)
    authorization_boundary_diagram = models.ForeignKey(attachment, on_delete=models.PROTECT,
                                                       related_name='system_authorization_boundary_diagram', blank=True,
                                                       null=True)
    network_architecture_diagram = models.ForeignKey(attachment, on_delete=models.PROTECT,
                                                     related_name='system_network_architecture_diagram', blank=True,
                                                     null=True)
    data_flow_diagram = models.ForeignKey(attachment, on_delete=models.PROTECT, related_name='system_data_flow_diagram',
                                          blank=True, null=True)

    def _get_selected_controls(self):
        selected_controls = self.control_baseline.controls
        for item in self.additional_selected_controls.all():
            selected_controls.add(item)
        return selected_controls

    @property
    def selected_controls(self):
        return self._get_selected_controls()


"""
***********************************************************
******************  Serializer Classes  *******************
***********************************************************
"""

class system_user_serializer(serializers.ModelSerializer):
    roles = user_role_serializer(many=True, read_only=True)

    class Meta:
        model = system_user
        fields = ['id', 'uuid', 'title', 'short_name', 'desc', 'remarks', 'roles']
        depth = 1

