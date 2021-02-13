from django.db import models
from rest_framework_tricks.models.fields import NestedProxyField
from tinymce.models import HTMLField
from django.utils import timezone
import uuid
from django.template.defaultfilters import truncatechars


from scripts.usefullFunctions import serializerJSON
from rest_framework_json_api import serializers

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
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

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

    @staticmethod
    def get_serializer_json(id=1):
        queryset = element_property.objects.filter(pk=id)
        serializer = element_property_serializer(queryset, many=True)
        return (serializerJSON(serializer.data))

    @property
    def get_serializer_json_OSCAL(self):
        queryset = element_property.objects.filter(pk=self.pk)
        serializer = element_property_serializer(queryset, many=True)
        return (serializerJSON(serializer.data, SSP=True))



class hashed_value(BasicModel):
    """
    used to store hashed values for validation of attachments or linked files
    """
    value = customTextField()
    algorithm = models.CharField(max_length=100)

    @staticmethod
    def get_serializer_json(id=1):
        queryset = hashed_value.objects.filter(pk=id)
        serializer = hashed_value_serializer(queryset, many=True)
        return (serializerJSON(serializer.data))

    @property
    def get_serializer_json_OSCAL(self):
        queryset = hashed_value.objects.filter(pk=self.pk)
        serializer = hashed_value_serializer(queryset, many=True)
        return (serializerJSON(serializer.data, SSP=True))



class link(PrimitiveModel):
    text = models.CharField(max_length=255)
    href = models.CharField(max_length=255)
    requires_authentication = models.BooleanField(default=False)
    rel = models.CharField(max_length=255, blank=True)
    mediaType = models.CharField(max_length=255, blank=True)
    hash = models.ForeignKey(hashed_value, on_delete=models.PROTECT, null=True, blank=True, related_name='link_set')
    #: Added related_name='link_set' to be used in creating the serializers.

    def __str__(self):
        return self.text

    @staticmethod
    def get_serializer_json(id=1):
        queryset = link.objects.filter(pk=id)
        serializer = link_serializer(queryset, many=True)
        return (serializerJSON(serializer.data))

    @property
    def get_serializer_json_OSCAL(self):
        queryset = link.objects.filter(pk=self.pk)
        serializer = link_serializer(queryset, many=True)
        return (serializerJSON(serializer.data, SSP=True))



class annotation(BasicModel):
    annotationID = models.CharField(max_length=25)
    ns = models.CharField(max_length=100)
    value = customTextField()

    @staticmethod
    def get_serializer_json(id=1):
        queryset = annotation.objects.filter(pk=id)
        serializer = annotation_serializer(queryset, many=True)
        return (serializerJSON(serializer.data))

    @property
    def get_serializer_json_OSCAL(self):
        queryset = annotation.objects.filter(pk=self.pk)
        serializer = annotation_serializer(queryset, many=True)
        return (serializerJSON(serializer.data, SSP=True))



class ExtendedBasicModel(BasicModel):
    """
    Basic fields plus properties, annotations, and links
    """
    properties = customMany2ManyField(element_property)
    annotations = customMany2ManyField(annotation)
    links = customMany2ManyField(link)

    class Meta:
        abstract = True


"""
***********************************************************
******************  Serializer Classes  *******************
***********************************************************
"""

class element_property_serializer(serializers.ModelSerializer):

    class Meta:
        model = element_property
        fields = ['id', 'uuid', 'value', 'name', 'property_id', 'ns', 'prop_class']



class link_serializer(serializers.ModelSerializer):

    class Meta:
        model = link
        fields = ['id', 'uuid', 'text', 'href', 'requires_authentication', 'rel', 'mediaType', 'hash_id']
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



class annotation_serializer(serializers.ModelSerializer):

    class Meta:
        model = annotation
        fields = ['id', 'uuid', 'annotationID','ns','value', 'title', 'short-name', 'description', 'remarks']

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }

