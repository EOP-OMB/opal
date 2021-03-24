from ssp.models.common import *

# elements of a user, role, and group
class user_function(BasicModel):
    """
    list of functions assigned to roles. e.g. backup servers, deploy software, etc.
    """

    @property
    def get_serializer_json_OSCAL(self):
        queryset = user_function.objects.filter(pk=self.pk)
        serializer = user_function_serializer(queryset, many=True)
        return (serializerJSON(serializer.data, SSP=True))



class user_privilege(BasicModel):
    functionsPerformed = customMany2ManyField(user_function)

    @property
    def get_serializer_json_OSCAL(self):
        queryset = user_privilege.objects.filter(pk=self.pk)
        serializer = user_privilege_serializer(queryset, many=True)
        return (serializerJSON(serializer.data, SSP=True))



class user_role(ExtendedBasicModel):
    user_privileges = customMany2ManyField(user_privilege)

    @property
    def get_serializer_json_OSCAL(self):
        queryset = user_role.objects.filter(pk=self.pk)
        serializer = user_role_serializer(queryset, many=True)
        return (serializerJSON(serializer.data, SSP=True))



# elements that can apply to a user, organization or both
class address(BasicModel):
    type = models.CharField(max_length=100)
    postal_address = customTextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    postal_code = models.CharField(max_length=25)
    country = models.CharField(max_length=100)

    @property
    def get_serializer_json_OSCAL(self):
        queryset = address.objects.filter(pk=self.pk)
        serializer = address_serializer(queryset, many=True)
        return (serializerJSON(serializer.data, SSP=True))



class email(PrimitiveModel):
    email = models.EmailField()
    type = models.CharField(max_length=50, choices=contactInfoType, default='work')
    supports_rich_text = models.BooleanField(default=True)

    def __str__(self):
        return self.type + ': ' + self.email

    @property
    def get_serializer_json_OSCAL(self):
        queryset = email.objects.filter(pk=self.pk)
        serializer = email_serializer(queryset, many=True)
        return (serializerJSON(serializer.data, SSP=True))



class telephone_number(PrimitiveModel):
    number = models.CharField(max_length=25)
    type = models.CharField(max_length=25)

    def __str__(self):
        return self.type + ': ' + self.number

    @property
    def get_serializer_json_OSCAL(self):
        queryset = telephone_number.objects.filter(pk=self.pk)
        serializer = telephone_number_serializer(queryset, many=True)
        return (serializerJSON(serializer.data, SSP=True))



class location(ExtendedBasicModel):
    address = models.ForeignKey(address, on_delete=models.PROTECT, related_name='location_set')
    emailAddresses = customMany2ManyField(email)
    telephoneNumbers = customMany2ManyField(telephone_number)


    @property
    def get_serializer_json_OSCAL(self):
        queryset = location.objects.filter(pk=self.pk)
        serializer = location_serializer(queryset, many=True)
        return (serializerJSON(serializer.data, SSP=True))


class organization(ExtendedBasicModel):
    """
    Groups of people
    """
    locations = customMany2ManyField(location)
    email_addresses = customMany2ManyField(email)
    telephone_numbers = customMany2ManyField(telephone_number)


    @property
    def get_serializer_json_OSCAL(self):
        queryset = organization.objects.filter(pk=self.pk)
        serializer = organization_serializer(queryset, many=True)
        return (serializerJSON(serializer.data, SSP=True))



class person(ExtendedBasicModel):
    """
    An individual who can be assigned roles within a system.
    """

    class Meta:
        ordering = ('name',)

    name = models.CharField(max_length=100)
    organizations = customMany2ManyField(organization)
    locations = customMany2ManyField(location)
    email_addresses = customMany2ManyField(email)
    telephone_numbers = customMany2ManyField(telephone_number)

    def __str__(self):
        return self.name


    @property
    def get_serializer_json_OSCAL(self):
        queryset = person.objects.filter(pk=self.pk)
        serializer = person_serializer(queryset, many=True)
        return (serializerJSON(serializer.data, SSP=True))


"""
***********************************************************
******************  Serializer Classes  *******************
***********************************************************
"""

class user_function_serializer(serializers.ModelSerializer):

    class Meta:
        model = user_function
        fields = ['id', 'uuid', 'title', 'short-name', 'description', 'remarks']

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }



class user_privilege_serializer(serializers.ModelSerializer):
    functionsPerformed = user_function_serializer(read_only=True, many=True)

    class Meta:
        model = user_privilege
        fields= ['id', 'uuid', 'title', 'short-name', 'description', 'remarks','functionsPerformed']

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }



class user_role_serializer(serializers.ModelSerializer):
    user_privileges = user_privilege_serializer(read_only=True, many=True)

    class Meta:
        model= user_role
        fields = ['id', 'uuid', 'title', 'short-name', 'description', 'remarks', 'properties','annotations','links','user_privileges']

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }



class email_serializer(serializers.ModelSerializer):

    class Meta:
        model = email
        fields = ['id', 'uuid', 'email', 'type', 'supports_rich_text']

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }



class telephone_number_serializer(serializers.ModelSerializer):

    class Meta:
        model = telephone_number
        fields = ['id', 'uuid', 'number', 'type']

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }



class location_serializer(serializers.ModelSerializer):
    emailAddresses = email_serializer(many=True, read_only=True)
    telephoneNumbers = telephone_number_serializer(many=True, read_only=True)

    class Meta:
        model = location
        fields = ['id', 'uuid', 'title', 'short-name', 'description', 'remarks', 'properties','annotations','links', 'emailAddresses', 'telephoneNumbers','address_id']
        depth = 1

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }



class address_serializer(serializers.ModelSerializer):
    location_set = location_serializer(many=True, read_only=True)

    class Meta:
        model = address
        fields = ['id', 'uuid', 'title', 'short-name', 'description', 'remarks', 'type', 'postal_address', 'city', 'state', 'postal_code', 'country', 'location_set']

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }



class organization_serializer(serializers.ModelSerializer):
    locations = location_serializer(many=True, read_only=True)
    email_addresses = email_serializer(many=True, read_only=True)
    telephone_numbers = telephone_number_serializer(many=True, read_only=True)

    class Meta:
        model = organization
        fields = ['id', 'uuid', 'title', 'short-name', 'description', 'remarks', 'properties','annotations','links', 'locations', 'email_addresses', 'telephone_numbers']

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }



class person_serializer(serializers.ModelSerializer):
    organizations = organization_serializer(many=True, read_only=True)
    locations = location_serializer(many=True, read_only=True)
    email_addresses = email_serializer(many=True, read_only=True)
    telephone_numbers = telephone_number_serializer(many=True, read_only=True)

    class Meta:
        model = person
        fields = ['id', 'uuid', 'title', 'short-name', 'description', 'remarks', 'properties','annotations','links', 'name', 'organizations', 'locations', 'email_addresses', 'telephone_numbers']

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }
