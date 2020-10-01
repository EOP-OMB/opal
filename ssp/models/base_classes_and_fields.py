from django.db import models
from tinymce.models import HTMLField
import uuid

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


class hashed_value(BasicModel):
    """
    used to store hashed values for validation of attachments or linked files
    """
    value = customTextField()
    algorithm = models.CharField(max_length=100)


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