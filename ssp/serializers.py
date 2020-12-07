from rest_framework_json_api import serializers
from ssp.models.base_classes_and_fields import *
from ssp.models.controls import *
from ssp.models.common import *
from ssp.models.systems import *
from ssp.models.users import *


class element_property_serializer(serializers.ModelSerializer):

    class Meta:
        model = element_property
        fields = ['id', 'uuid', 'value', 'name', 'property_id', 'ns', 'prop_class']


class link_serializer(serializers.ModelSerializer):

    class Meta:
        model = link
        fields = ['id', 'uuid', 'text', 'href', 'requires_authentication', 'rel', 'mediaType']
        depth = 1


class hashed_value_serializer(serializers.ModelSerializer):
    link_set = link_serializer(many=True, read_only=True)

    class Meta:
        model = hashed_value
        fields = ['id', 'uuid', 'title', 'short_name', 'desc', 'remarks', 'value', 'algorithm', 'link_set']


class annotation_serializer(serializers.ModelSerializer):

    class Meta:
        model = annotation
        fields = '__all__'

class ExtendedBasicModel_serializer(serializers.ModelSerializer):
    properties = element_property_serializer(read_only=True, many=True)
    annotations = annotation_serializer(read_only=True, many=True)
    links = link_serializer(read_only=True, many=True)
    class Meta:
        model = ExtendedBasicModel
        fields = ['id','uuid', 'title', 'short_name', 'desc', 'remarks', 'properties','annotations','links']


class information_type_serializer(serializers.ModelSerializer):

    class Meta:
        model = information_type
        fields = ['id', 'uuid', 'title', 'short_name', 'desc', 'remarks', 'confidentialityImpact','integrityImpact','availabilityImpact']


class user_function_serializer(serializers.ModelSerializer):

    class Meta:
        model = user_function
        fields=[]


class user_privilege_serializer(serializers.ModelSerializer):
    functionPerformed = user_function_serializer(read_only=True, many=True)

    class Meta:
        model = user_privilege
        fields= ['functionsPerformed']


class user_role_serializer(serializers.ModelSerializer):
    user_privilege = user_privilege_serializer(read_only=True, many=True)

    class Meta:
        model= user_role
        fields = ['user_privileges']


class system_component_serializer(serializers.ModelSerializer):
    properties = element_property_serializer(read_only=True, many=True)
    annotations = annotation_serializer(read_only=True, many=True)
    links = link_serializer(read_only=True, many=True)
    component_information_types = information_type_serializer(read_only=True, many=True)
    component_responsible_roles = user_role_serializer(read_only=True, many=True)

    class Meta:
        model = system_component
        fields = ['id', 'uuid', 'title', 'short_name', 'desc', 'remarks', 'properties','annotations','links', 'component_type', 'component_title', 'component_description', 'component_information_types', 'component_status', 'component_responsible_roles']
        depth = 1


class status_serializer(serializers.ModelSerializer):
    component_status_set = system_component_serializer(many=True, read_only=True)

    class Meta:
        model = status
        fields = ['id', 'uuid', 'state', 'title', 'short_name', 'desc', 'remarks', 'component_status_set']


class email_serializer(serializers.ModelSerializer):

    class Meta:
        model = email
        fields = ['id', 'uuid', 'email', 'type', 'supports_rich_text']


class telephone_number_serializer(serializers.ModelSerializer):

    class Meta:
        model = telephone_number
        fields = ['id', 'uuid', 'number', 'type']


class location_serializer(serializers.ModelSerializer):
    emailAddresses = email_serializer(many=True, read_only=True)
    telephoneNumbers = telephone_number_serializer(many=True, read_only=True)

    class Meta:
        model = location
        fields = ['id', 'uuid', 'title', 'short_name', 'desc', 'remarks', 'properties','annotations','links', 'emailAddresses', 'telephoneNumbers']
        depth = 1


class address_serializer(serializers.ModelSerializer):
    location_set = location_serializer(many=True, read_only=True)

    class Meta:
        model = address
        fields = ['id', 'uuid', 'title', 'short_name', 'desc', 'remarks', 'properties', 'type', 'postal_address', 'city', 'state', 'postal_code', 'country', 'location_set']


class organization_serializer(serializers.ModelSerializer):
    locations = location_serializer(many=True, read_only=True)
    email_addresses = email_serializer(many=True, read_only=True)
    telephone_numbers = telephone_number_serializer(many=True, read_only=True)

    class Meta:
        model = organization
        fields=['locations', 'email_addresses', 'telephone_number']


class system_user_serializer(serializers.ModelSerializer):
    roles = user_role_serializer(many=True, read_only=True)

    class Meta:
        model = system_user
        fields = ['id', 'uuid', 'title', 'short_name', 'desc', 'remarks', 'roles']
        depth = 1


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
        'description': {'source': 'desc'},
        }


class organizatioin_serializer(serializers.ModelSerializer):
    locations = location_serializer(many=True, read_only=True)
    email_addresses = email_serializer(many=True, read_only=True)
    telephone_numbers = telephone_number_serializer(many=True, read_only=True)

    class Meta:
        model = organization
        fields = ['id', 'uuid', 'title', 'short_name', 'desc', 'remarks', 'properties','annotations','links', 'locations','email_addresses','telephone_numbers']