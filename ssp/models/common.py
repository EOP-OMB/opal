from ssp.models.base_classes_and_fields import *


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
    fisma_levels = [('High', "High"), ('Moderate', "Moderate"), ('Low', "Low")]

    confidentialityImpact = models.CharField(max_length=50, choices=fisma_levels)
    integrityImpact = models.CharField(max_length=50, choices=fisma_levels)
    availabilityImpact = models.CharField(max_length=50, choices=fisma_levels)


# Other common objects used in many places
class attachment(ExtendedBasicModel):
    attachment_type = models.CharField(max_length=50, choices=attachment_types)
    attachment = models.FileField()
    filename = models.CharField(max_length=100, blank=True)
    mediaType = models.CharField(max_length=100, blank=True)
    hash = models.ForeignKey(hashed_value, on_delete=models.PROTECT, null=True)
    caption = models.CharField(max_length=200, blank=True)
