from datetime import datetime

from django import forms
from django.forms.widgets import SelectDateWidget, DateTimeInput
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from common.models import locations, parties, base64, system_status_state_choices
from ctrl_profile.models import ctrl_profiles
from component.models import components
from ssp.models import system_security_plans, information_types, inventory_items, security_sensitivity_level_choices


class system_security_plansForm(forms.Form):
    # metadata
    title = forms.CharField(help_text='A name given to the document, which may be used by a tool for display and navigation.', label='Document Title', max_length=1024)
    published = forms.DateTimeField(help_text='The date and time the document was published. The date-time value must be formatted according to RFC 3339 with full time and time zone included.', label='Publication Timestamp', widget=DateTimePickerInput, initial=datetime.now())
    last_modified = forms.DateTimeField(help_text='The date and time the document was last modified. The date-time value must be formatted according to RFC 3339 with full time and time zone included.', label='Last Modified Timestamp', widget=DateTimePickerInput, initial=datetime.now())
    version = forms.CharField(help_text='A string used to distinguish the current version of the document from other previous (and future) versions.', initial='1.0', label='Document Version', max_length=1024)
    oscal_version = forms.CharField(help_text='The OSCAL model version the document was authored against.', initial='v1.0.3', label='OSCAL Version', max_length=1024)
    locations = forms.ModelMultipleChoiceField(queryset=locations.objects.all(), label='Locations', required=False)
    responsible_parties = forms.ModelMultipleChoiceField(queryset=parties.objects.all(), help_text='A reference to a set of organizations or persons that have responsibility for performing a referenced role in the context of the containing object.', label='Responsible Parties', required=False)
    import_profile = forms.ModelChoiceField(queryset=ctrl_profiles.objects.all(), label='Import profile', required=False)
    # system_characteristics
    system_name = forms.CharField(help_text='The full name of the system.', label='System Name - Full', max_length=1024)
    system_name_short = forms.CharField(help_text='A short name for the system, such as an acronym, that is suitable for display in a data table or summary list.', label='System Name - Short', max_length=1024)
    description = forms.CharField(help_text='A summary of the system.', label='System Description')
    security_sensitivity_level = forms.TypedChoiceField(help_text='The overall information system sensitivity categorization, such as defined by FIPS-199.', label='Security Sensitivity Level', choices=security_sensitivity_level_choices)
    security_impact_level = forms.TypedChoiceField(help_text='The overall level of expected impact resulting from unauthorized disclosure, modification, or loss of access to information.', label='Security Impact Level', choices=security_sensitivity_level_choices)
    security_objective_confidentiality = forms.TypedChoiceField(help_text='A target-level of confidentiality for the system, based on the sensitivity of information within the system.', label='Security Objective: Confidentiality', choices=security_sensitivity_level_choices)
    security_objective_integrity = forms.TypedChoiceField(help_text='A target-level of integrity for the system, based on the sensitivity of information within the system.', label='Security Objective: Integrity', choices=security_sensitivity_level_choices)
    security_objective_availability = forms.TypedChoiceField(help_text='A target-level of availability for the system, based on the sensitivity of information within the system.', label='Security Objective: Availability', choices=security_sensitivity_level_choices)
    status = forms.TypedChoiceField(help_text='Describes the operational status of the system.', label='Status', choices=system_status_state_choices)
    authorization_boundary = forms.ModelChoiceField(queryset=base64.objects.all(), help_text="A description of this system's authorization boundary, optionally supplemented by diagrams that illustrate the authorization boundary.", label='Authorization Boundary', required=False)
    network_architecture = forms.ModelChoiceField(queryset=base64.objects.all(), help_text="A description of the system's network architecture, optionally supplemented by diagrams that illustrate the network architecture.", label='Network Architecture', required=False)
    data_flow = forms.ModelChoiceField(queryset=base64.objects.all(), help_text="A description of the system's data flow, optionally supplemented by diagrams that illustrate the data flow.", label='Data Flow', required=False)
    system_information_types = forms.ModelMultipleChoiceField(queryset=information_types.objects.all(), help_text='Contains details about all information types that are stored, processed, or transmitted by the system, such as privacy information, and those defined in NIST SP 800-60.', label='System Information Types', required=False)
    # system_implementation
    leveraged_authorizations = forms.ModelMultipleChoiceField(queryset=system_security_plans.objects.all(), help_text='A description of another authorized system from which this system inherits capabilities that satisfy security requirements. Another term for this concept is a common control provider.', label='Leveraged Authorizations', required=False)
    components = forms.ModelMultipleChoiceField(queryset=components.objects.all(), help_text='A defined component that can be part of an implemented system. Components may be products, services, application programming interface (APIs), policies, processes, plans, guidance, standards, or other tangible items that enable security and/or privacy.', label='Components', required=False)
    inventory_items = forms.ModelMultipleChoiceField(queryset=inventory_items.objects.all(), help_text='A set of inventory-item entries that represent the managed inventory instances of the system.', label='Inventory Items', required=False)


