from ssp.models.controls import *

type_choices = [("splunk","Splunk Search"),
            ("shell", "Shell Command"),
            ("curl", "Curl Command")]

class test_evidence(ExtendedBasicModel):
    """
    Evidence outcome from Tests
    """
    type = models.CharField(max_length=255, choices=type_choices)
    testing_conditions = models.CharField(max_length=2000)
    results = customMany2ManyField(attachment)
    controls = customMany2ManyField(system_control)
