from ssp.models.base_classes_and_fields import *

# True lookup tables for storing select values
class status(BasicModel):
    # system implementation status. Normally operational, under-development,
    # under-major-modification, disposition, and other but users can add custom options
    state = models.CharField(max_length=30)

    @staticmethod
    def get_serializer_json(id=1):
        queryset = status.objects.filter(pk=id)
        serializer = status_serializer(queryset, many=True)
        return (serializerJSON(serializer.data))


class information_type(BasicModel):
    """
    Management and support information and information systems impact levels
    as defined in NIST SP 800-60 APPENDIX C. Additional information types may be added
    by the user
    """
    fisma_levels = [('High', "High"), ('Moderate', "Moderate"), ('Low', "Low")]

    confidentialityImpact = models.CharField(max_length=50, choices=fisma_levels)
    integrityImpact = models.CharField(max_length=50, choices=fisma_levels)
    availabilityImpact = models.CharField(max_length=50, choices=fisma_levels)

    @staticmethod
    def get_serializer_json(id=1):
        queryset = information_type.objects.filter(pk=id)
        serializer = information_type_serializer(queryset, many=True)
        return (serializerJSON(serializer.data))


# Other common objects used in many places
class attachment(ExtendedBasicModel):
    attachment_type = models.CharField(max_length=50, choices=attachment_types)
    attachment = models.FileField()
    filename = models.CharField(max_length=100, blank=True)
    mediaType = models.CharField(max_length=100, blank=True)
    hash = models.ForeignKey(hashed_value, on_delete=models.PROTECT, null=True, blank=True, related_name='attachment_set')
    caption = models.CharField(max_length=200, blank=True)

    @staticmethod
    def get_serializer_json(id=1):
        queryset = attachment.objects.filter(pk=id)
        serializer = attachment_serializer(queryset, many=True)
        return (serializerJSON(serializer.data))


"""
***********************************************************
******************  Serializer Classes  *******************
***********************************************************
"""


class status_serializer(serializers.ModelSerializer):

    class Meta:
        model = status
        fields = ['id', 'uuid', 'state', 'title', 'short_name', 'desc', 'remarks', 'state']


class information_type_serializer(serializers.ModelSerializer):

    class Meta:
        model = information_type
        fields = ['id', 'uuid', 'title', 'short_name', 'desc', 'remarks', 'confidentialityImpact','integrityImpact','availabilityImpact']


class attachment_serializer(serializers.ModelSerializer):

    class Meta:
        model = attachment
        fields = ['id', 'uuid', 'title', 'short_name', 'desc', 'remarks', 'properties','annotations','links', 'attachment_type', 'attachment', 'filename', 'mediaType', 'caption']
        depth = 1