from common.models import BasicModel, CustomManyToManyField, PrimitiveModel, ShortTextField

from ssp.models.controls import *

type_choices = [("splunk_search","Splunk Search"),
            ("splunk_report","Splunk Report"),
            ("shell", "Shell Command"),
            ("curl", "Curl Command")]

class test_evidence(ExtendedBasicModel):
    """
    Evidence outcome from Tests
    """
    type = models.CharField(max_length=255, choices=type_choices)
    testing_conditions = models.CharField(max_length=2000)
    results = customMany2ManyField(attachment) 
    numberResults = models.PositiveSmallIntegerField(default=1)
    controls = customMany2ManyField(system_control)

