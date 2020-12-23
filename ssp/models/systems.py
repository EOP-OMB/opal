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
    component_status = models.ForeignKey(status, on_delete=models.PROTECT, null=True, related_name='system_component_set')
    component_responsible_roles = customMany2ManyField(user_role)

    @staticmethod
    def get_serializer_json(id=1):
        queryset = system_component.objects.filter(pk=id)
        serializer = system_component_serializer(queryset, many=True)
        return (serializerJSON(serializer.data))



class port_range(BasicModel):
    start = models.IntegerField()
    end = models.IntegerField()
    transport = models.CharField(max_length=40)

    def __str__(self):
        r = str(self.start) + '-' + str(self.end) + ' ' + self.transport
        return r

    @staticmethod
    def get_serializer_json(id=1):
        queryset = port_range.objects.filter(pk=id)
        serializer = port_range_serializer(queryset, many=True)
        return (serializerJSON(serializer.data))



class protocol(BasicModel):
    portRanges = customMany2ManyField(port_range)

    @staticmethod
    def get_serializer_json(id=1):
        queryset = protocol.objects.filter(pk=id)
        serializer = protocol_serializer(queryset, many=True)
        return (serializerJSON(serializer.data))



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

    @staticmethod
    def get_serializer_json(id=1):
        queryset = system_service.objects.filter(pk=id)
        serializer = system_service_serializer(queryset, many=True)
        return (serializerJSON(serializer.data))



class system_interconnection(ExtendedBasicModel):
    interconnection_responsible_roles = customMany2ManyField(user_role)

    @staticmethod
    def get_serializer_json(id=1):
        queryset = system_interconnection.objects.filter(pk=id)
        serializer = system_interconnection_serializer(queryset, many=True)
        return (serializerJSON(serializer.data))



class inventory_item_type(ExtendedBasicModel):
    """
    generic role of an inventory item. For example, webserver, database server, network switch, edge router.
    All inventory items should be classified into an inventory item type
    """
    use = customTextField()
    responsibleRoles = customMany2ManyField(user_role)
    baseline_configuration = models.ForeignKey(link, on_delete=models.PROTECT, blank=True,
                                               related_name='baseline_configuration')

    @staticmethod
    def get_serializer_json(id=1):
        queryset = inventory_item_type.objects.filter(pk=id)
        serializer = inventory_item_type_serializer(queryset, many=True)
        return (serializerJSON(serializer.data))



class system_inventory_item(ExtendedBasicModel):
    """
    Physical (or virtual) items which make up the information system.
    """
    inventory_item_type = models.ForeignKey(inventory_item_type, on_delete=models.PROTECT, related_name='system_inventory_item_set')
    item_special_configuration_settings = customTextField()

    @staticmethod
    def get_serializer_json(id=1):
        queryset = system_inventory_item.objects.filter(pk=id)
        serializer = system_inventory_item_serializer(queryset, many=True)
        return (serializerJSON(serializer.data))



class system_user(BasicModel):
    user = models.ForeignKey(person, on_delete=models.PROTECT, related_name='system_user_set')
    roles = customMany2ManyField(user_role)

    @staticmethod
    def get_serializer_json(id=1):
        queryset = system_user.objects.filter(pk=id)
        serializer = system_user_serializer(queryset, many=True)
        return (serializerJSON(serializer.data))



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
    control_baseline = models.ForeignKey(control_baseline, on_delete=models.PROTECT, null=True, related_name='ssp_control_baseline_set')
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
    system_status = models.ForeignKey(status, on_delete=models.PROTECT, null=True, related_name='ssp_system_status_set')
    authorization_boundary_diagram = models.ForeignKey(attachment, on_delete=models.PROTECT,
                                                       related_name='system_authorization_boundary_diagram', blank=True,
                                                       null=True)
    network_architecture_diagram = models.ForeignKey(attachment, on_delete=models.PROTECT,
                                                     related_name='system_network_architecture_diagram', blank=True,
                                                     null=True)
    data_flow_diagram = models.ForeignKey(attachment, on_delete=models.PROTECT, related_name='system_data_flow_diagram',
                                          blank=True, null=True)

    """
    Samira: NestedProxyFields are added to make the JSON export match with OSCAL format. They don't change the table definition in the database. 
    Each NestedProxyField needs a serializer and the main serializer uses them in the field section.
    """
    metadata = NestedProxyField('title', 'published', 'lastModified', 'version','oscalVersion', 'properties', 'annotations', 'links', 'remarks')
    system_information = NestedProxyField('information_types')
    security_impact_level = NestedProxyField('security_objective_confidentiality', 'security_objective_integrity', 'security_objective_availability')
    system_characteristics = NestedProxyField('short_name', 'desc', 'date_authorized', 'security_sensitivity_level', 'system_information', 'security_impact_level', 'system_status', 'authorization_boundary_diagram',
                              'network_architecture_diagram', 'data_flow_diagram')
    system_implementation = NestedProxyField('leveraged_authorization', 'system_users', 'system_components', 'system_inventory_items')
    control_implementation = NestedProxyField('controls')


    def _get_selected_controls(self):
        selected_controls = self.control_baseline.controls
        for item in self.additional_selected_controls.all():
            selected_controls.add(item)
        return selected_controls.order_by('sort_id')

    @property
    def selected_controls(self):
        return self._get_selected_controls()

    @staticmethod
    def get_serializer_json(id=1):
        queryset = system_security_plan.objects.filter(pk=id)
        serializer = system_security_plan_serializer(queryset, many=True)
        return (serializerJSON(serializer.data))

    @staticmethod
    def get_serializer_json_OSCAL(id=1):
        queryset = system_security_plan.objects.filter(pk=id)
        serializer = system_security_plan_OSCAL_serializer(queryset, many=True)
        return (serializerJSON(serializer.data))


"""
***********************************************************
******************  Serializer Classes  *******************
***********************************************************
"""

class system_component_serializer(serializers.ModelSerializer):
    properties = element_property_serializer(read_only=True, many=True)
    annotations = annotation_serializer(read_only=True, many=True)
    links = link_serializer(read_only=True, many=True)
    component_information_types = information_type_serializer(read_only=True, many=True)
    component_responsible_roles = user_role_serializer(read_only=True, many=True)

    class Meta:
        model = system_component

        fields = ['id', 'uuid', 'title', 'short-name', 'description', 'remarks', 'properties','annotations','links', 'component_type', 'component_title', 'component_description', 'component_information_types', 'component_status', 'component_responsible_roles']
        depth = 1

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }



class port_range_serializer(serializers.ModelSerializer):

    class Meta:
        model = port_range
        fields = ['id', 'uuid', 'title', 'short-name', 'description', 'remarks','start', 'end', 'transport']

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }



class protocol_serializer(serializers.ModelSerializer):
    portRanges = port_range_serializer(read_only=True, many=True)
    class Meta:
        model = protocol
        fields = ['id', 'uuid', 'title', 'short-name', 'description', 'remarks', 'portRanges']

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }



class system_service_serializer(serializers.ModelSerializer):
    protocols = protocol_serializer(read_only=True, many=True)
    service_information_types = information_type_serializer(read_only=True, many=True)

    class Meta:
        model = system_service
        fields = ['id', 'uuid', 'title', 'short-name', 'description', 'remarks','properties','annotations','links',
                  'protocols', 'service_purpose', 'service_information_types']

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }



class system_interconnection_serializer(serializers.ModelSerializer):
    interconnection_responsible_roles = user_role_serializer(read_only=True, many=True)

    class Meta:
        model = system_interconnection
        fields = ['id', 'uuid', 'title', 'short-name', 'description', 'remarks','properties','annotations','links',
                  'interconnection_responsible_roles']

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }



class system_user_serializer(serializers.ModelSerializer):
    roles = user_role_serializer(many=True, read_only=True)
    user = person_serializer(many=False, read_only=True)

    class Meta:
        model = system_user
        fields = ['id', 'uuid', 'title', 'short-name', 'description', 'remarks', 'roles','user']
        depth = 1

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }



class system_inventory_item_serializer(serializers.ModelSerializer):

    class Meta:
        model = system_inventory_item
        fields = ['id', 'uuid', 'title', 'short-name', 'description', 'remarks', 'properties', 'annotations', 'links',
                  'item_special_configuration_settings','inventory_item_type']
        depth = 1

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }



class inventory_item_type_serializer(serializers.ModelSerializer):
    responsibleRoles = user_role_serializer(read_only=True, many=True)
    system_inventory_item_set = system_inventory_item_serializer(read_only=True, many=True)

    class Meta:
        model = inventory_item_type
        fields = ['id', 'uuid', 'title', 'short-name', 'description', 'remarks', 'properties', 'annotations', 'links',
                  'use', 'responsibleRoles', 'system_inventory_item_set', 'baseline_configuration_id']
        depth = 1

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }


class leveraged_authorization_serializer(serializers.ModelSerializer):
    class Meta:
        model = system_security_plan
        fields = ['id', 'uuid', 'title', 'short-name', 'description', 'properties', 'annotations', 'links', 'date_authorized','remarks']

    extra_kwargs = {
        'short-name': {'source': 'short_name'},
        'description': {'source': 'desc'}
    }



class system_security_plan_serializer(serializers.ModelSerializer):
    system_components = system_component_serializer(read_only=True, many=True)
    system_services = system_service_serializer(read_only=True, many=True)
    system_interconnections = system_interconnection_serializer(read_only=True, many=True)
    system_inventory_items = system_inventory_item_serializer(read_only=True, many=True)
    additional_selected_controls = nist_control_serializer(read_only=True, many=True)
    leveraged_authorization = leveraged_authorization_serializer(read_only=True, many=True)
    controls = system_control_serializer(read_only=True, many=True)
    system_users = system_user_serializer(read_only=True, many=True)
    information_types = information_type_serializer(read_only=True, many=True)

    system_status = status_serializer(read_only=True, many=False)
    authorization_boundary_diagram = attachment_serializer(read_only=True, many=False)
    network_architecture_diagram = attachment_serializer(read_only=True, many=False)
    data_flow_diagram = attachment_serializer(read_only=True, many=False)

    class Meta:
        model = system_security_plan
        fields = ['id', 'uuid', 'title', 'short-name', 'description', 'remarks', 'properties', 'annotations', 'links', 'published', 'lastModified',
                  'version','oscalVersion', 'leveraged_authorization', 'system_components', 'system_services', 'system_interconnections', 'system_inventory_items',
                  'additional_selected_controls', 'controls', 'system_users', 'date_authorized', 'security_sensitivity_level',
                  'information_types', 'security_objective_confidentiality', 'security_objective_integrity', 'security_objective_availability',
                  'control_baseline_id', 'data_flow_diagram_id', 'authorization_boundary_diagram_id', 'network_architecture_diagram_id', 'system_status']
        depth = 1

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }



class metadata_serializer(serializers.ModelSerializer):
    properties = element_property_serializer(read_only=True, many=True)
    links = link_serializer(read_only=True, many=True)

    class Meta:
        model = system_security_plan
        fields = ['title', 'published', 'lastModified', 'version','oscalVersion', 'properties', 'annotations', 'links', 'remarks']





class system_information_serilaizer(serializers.ModelSerializer):
    information_types = information_type_serializer(read_only=True, many=True)

    class Meta:
        model = system_security_plan
        fields = ['information_types']



class security_impact_level_serializer(serializers.ModelSerializer):

    class Meta:
        model = system_security_plan
        fields = ['security_objective_confidentiality', 'security_objective_integrity', 'security_objective_availability']


class system_characteristics_serializer(serializers.ModelSerializer):
    system_information = system_information_serilaizer(required=False)
    security_impact_level = security_impact_level_serializer(required=False)
    system_status = status_serializer(read_only=True, many=False)
    authorization_boundary_diagram = attachment_serializer(read_only=True, many=False)
    network_architecture_diagram = attachment_serializer(read_only=True, many=False)
    data_flow_diagram = attachment_serializer(read_only=True, many=False)

    class Meta:
        model = system_security_plan
        fields = ['system_name', 'desc', 'date_authorized', 'security_sensitivity_level', 'system_information', 'security_impact_level', 'system_status', 'authorization_boundary_diagram',
                              'network_architecture_diagram', 'data_flow_diagram']

        extra_kwargs = {
            'system_name': {'source': 'short_name'}
        }



class system_control_serializer(serializers.ModelSerializer):
    """Samira: Redefined this serializer in this module to make the fields like format outline in OSCAL."""
    control_parameters = control_parameter_serializer(many=True, read_only=True)
    control_statements = control_statement_serializer(many=True, read_only=True)

    class Meta:
        model = system_control
        fields = ['uuid', 'control-id', 'properties', 'annotations', 'links', 'control_parameters', 'control_statements', 'remarks']

        depth = 1

        extra_kwargs = {
            'control-id': {'source': 'id'}
        }



class system_implementation_serializer(serializers.ModelSerializer):
    leveraged_authorization = leveraged_authorization_serializer(read_only=True, many=True)
    system_users = system_user_serializer(read_only=True, many=True)
    system_components = system_component_serializer(read_only=True, many=True)
    system_inventory_items = system_inventory_item_serializer(read_only=True, many=True)

    class Meta:
        model = system_security_plan
        fields = ['leveraged_authorization', 'system_users', 'system_components', 'system_inventory_items']



class control_implementation_serializer(serializers.ModelSerializer):
    controls = system_control_serializer(read_only=True, many=True)

    class Meta:
        model = system_security_plan
        fields = ['controls']


class system_security_plan_OSCAL_serializer(serializers.ModelSerializer):
    metadata = metadata_serializer(required=False)
    system_characteristics = system_characteristics_serializer(required=False)
    system_implementation = system_implementation_serializer(required=False)
    control_implementation = control_implementation_serializer(required=False)

    class Meta:
        model = system_security_plan
        fields = ['id', 'uuid', 'metadata', 'system_characteristics', 'system_implementation', 'control_implementation']



class link_serializer(serializers.ModelSerializer):
    inventory_item_type_set = inventory_item_type_serializer(read_only=True, many=True)

    class Meta:
        model = link
        fields = ['id', 'uuid', 'text', 'href', 'requires_authentication', 'rel', 'mediaType', 'inventory_item_type_set']
        depth = 1



class hashed_value_serializer(serializers.ModelSerializer):
    link_set = link_serializer(many=True, read_only=True)

    class Meta:
        model = hashed_value
        fields = ['id', 'uuid', 'title', 'short-name', 'description', 'remarks', 'value', 'algorithm', 'link_set']

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }



class person_serializer(serializers.ModelSerializer):
    organizations = organization_serializer(many=True, read_only=True)
    locations = location_serializer(many=True, read_only=True)
    email_addresses = email_serializer(many=True, read_only=True)
    telephone_numbers = telephone_number_serializer(many=True, read_only=True)
    system_user_set = system_user_serializer(many=True, read_only=True)

    class Meta:
        model = person
        fields = ['id', 'uuid', 'title', 'short-name', 'description', 'remarks', 'properties','annotations','links', 'name', 'organizations', 'locations', 'email_addresses', 'telephone_numbers','system_user_set']

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }



class control_baseline_serializer(serializers.ModelSerializer):
    controls = nist_control_serializer(many=True, read_only=True)
    ssp_control_baseline_set = system_security_plan_serializer(many=True, read_only=True)

    class Meta:
        model = control_baseline
        fields = ['id', 'uuid', 'title', 'short-name', 'description', 'remarks', 'controls', 'ssp_control_baseline_set']

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }



class system_control_serializer(serializers.ModelSerializer):
    parameter_settings = control_parameter_serializer(many=True, read_only=True)
    statements = control_statement_serializer(many=True, read_only=True)

    class Meta:
        model = system_control
        fields = ['uuid', 'control-id', 'props','annotations','links', 'parameter-settings', 'statements', 'remarks']
        depth = 1

        extra_kwargs = {
            'control-id': {'source': 'id'},
            'props': {'source': 'properties'},
            'description': {'source': 'desc'}
        }