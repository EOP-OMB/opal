from common.models import *
from catalog.models import controls


system_status_state_choices = [
        ("operational", "Operational: The system is currently operating in production."),
        ("under-development", "Under Development: The system is being designed, developed, or implemented"),
        ("under-major-modification",
         "Under Major Modification: The system is undergoing a major change, development, or transition."),
        ("disposition", "Disposition: The system is no longer operational."),
        ("other", "Other: Some other state, a remark must be included to describe the current state.")
        ]

class import_profiles(BasicModel):
    """
    Used to import the OSCAL profile representing the system's control baseline.
    """

    class Meta:
        verbose_name = "Import Profile"
        verbose_name_plural = "Import Profiles"

    href = ShortTextField(
        verbose_name="Profile Reference",
        help_text="A resolvable URL reference to the profile to use as the system's control baseline."
        )


class system_ids(PrimitiveModel):
    """
    A unique identifier for the system described by this system security plan.
    """

    class Meta:
        verbose_name = "System Identification"
        verbose_name_plural = "System Identifications"

    identifier_type = ShortTextField(
        verbose_name="Identification System Type",
        help_text="Identifies the identification system from which the provided identifier was assigned."
        )
    system_id = ShortTextField(verbose_name="System Identification")

    def __str__(self):
        return self.identifier_type + " - " + self.system_id

    def import_oscal(self, oscal_data,logger=None):
        if type(oscal_data) is dict:
            if "identifier_type" in oscal_data.keys():
                self.identifier_type = oscal_data["identifier_type"]
            if "system_id" in oscal_data.keys():
                self.system_id = oscal_data["system_id"]
        self.save()
        return self


class information_type_ids(PrimitiveModel):
    """
    An Information Type Categorization can actually have multiple information_type_ids associated with it and there is no guarantee that all of them would come from the internal system.  So we are providing a model here to hold all information type IDs for a categorization regardless of which system they come from.  In this developer's opinion, this part of the OSCAL Standard is overly confusing
    """

    class Meta:
        verbose_name = "Information Type Systematized Identifier"
        verbose_name_plural = "Information Type Systematized Identifiers"

    information_type_id = ShortTextField(
        verbose_name="Information Type Systematized Identifier",
        help_text="An identifier qualified by the given identification system used, such as NIST SP 800-60."
        )

    def import_oscal(self, oscal_data,logger=None):
        if type(oscal_data) is str:
            self.information_type_id = oscal_data
        return self


class categorizations(PrimitiveModel):
    """
    A set of information type identifiers qualified by the given identification system used, such as NIST SP 800-60.
    """

    class Meta:
        verbose_name = "Information Type Categorization"
        verbose_name_plural = "Information Type Categorizations"

    system = ShortTextField(
        verbose_name="Information Type Identification System",
        help_text="Specifies the information type identification system used."
        )
    information_type_ids = CustomManyToManyField(
        to=information_type_ids,
        verbose_name="Information Type Systematized Identifier",
        help_text="An identifier qualified by the given identification system used, such as NIST SP 800-60."
        )


class information_type_impact_level(BasicModel):
    """
    The base and adjusted security impact level of a specific requirement (Confidentiality, Accessibility, or Integrity) for a specific information type on a specific information system
    """

    class Meta:
        verbose_name = "Information Type Impact Level"
        verbose_name_plural = "Information Type Impact Levels"

    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    base = ShortTextField(
        verbose_name="Base Level (Confidentiality, Integrity, or Availability)",
        help_text="The prescribed base (Confidentiality, Integrity, or Availability) security impact level."
        )
    selected = ShortTextField(
        verbose_name="Selected Level (Confidentiality, Integrity, or Availability)",
        help_text="The selected (Confidentiality, Integrity, or Availability) security impact level.", null=True
        )
    adjustment_justification = models.TextField(
        verbose_name="Adjustment Justification",
        help_text="If the selected security level is different from the base security level, this contains the justification for the change.",
        null=True
        )

    def __str__(self):
        base = self.base
        if self.selected is None or len(self.selected) == 0:
            selected = base
        else:
            selected = self.selected
        if self.adjustment_justification is None:
            adjustment_justification = "Not Adjusted"
        else:
            adjustment_justification = self.adjustment_justification
        return "base: " + base + ", selected: " + selected + ", Justification: " + adjustment_justification

    @property
    def adjusted_impact_level(self):
        if self.selected is None or len(self.selected) == 0:
            return self.base
        else:
            return self.selected

    def import_oscal(self, oscal_data,logger=None):
        if type(oscal_data) is str:
            self.base = oscal_data
            self.save()
            return self
        else:
            oscal_data = self.fix_field_names(oscal_data)
            base = oscal_data["base"]
            if "selected" in oscal_data.keys():
                selected = oscal_data["selected"]
            else:
                selected = None
            if "adjustment_justification" in oscal_data.keys():
                adjustment_justification = oscal_data["adjustment_justification"]
            else:
                adjustment_justification = None
            obj, created = self._meta.model.objects.get_or_create(
                base=base, selected=selected, adjustment_justification=adjustment_justification
                )
            if "props" in oscal_data.keys():
                for item in oscal_data["props"]:
                    p = props.import_oscal(item)
                    obj.props.add(p)
            if "links" in oscal_data.keys():
                for item in oscal_data["links"]:
                    l = props.import_oscal(item)
                    obj.props.add(l)
            obj.save()
            return obj


class information_types(PrimitiveModel):
    title = ShortTextField(
        verbose_name="Information Type Title",
        help_text="A human readable name for the information type. This title should be meaningful within the context of the system."
        )
    description = ShortTextField(
        verbose_name="Information Type Description",
        help_text="A summary of how this information type is used within the system."
        )
    categorizations = CustomManyToManyField(
        to=categorizations, verbose_name="Information Type Categorization",
        help_text="A set of information type identifiers qualified by the given identification system used, such as NIST SP 800-60."
        )
    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    confidentiality_impact = models.ForeignKey(
        to=information_type_impact_level,
        verbose_name="Confidentiality Impact Level",
        help_text="The expected level of impact resulting from the unauthorized disclosure of the described information.",
        on_delete=models.CASCADE, related_name="confidentiality_impact"
        )
    integrity_impact = models.ForeignKey(
        to=information_type_impact_level,
        verbose_name="Integrity Impact Level",
        help_text="The expected level of impact resulting from the unauthorized modification of the described information.",
        on_delete=models.CASCADE, related_name="integrity_impact"
        )
    availability_impact = models.ForeignKey(
        to=information_type_impact_level, verbose_name="Availability Impact Level",
        help_text="The expected level of impact resulting from the disruption of access to or use of the described information or the information system.",
        on_delete=models.CASCADE, related_name="availability_impact"
        )

    def __str__(self):
        return self.title

    def to_html(self):

        html_str = "<div class='card shadow mb-4'>\n"
        html_str += "<!-- Card Header - Accordion -->\n"
        html_str += "<a href='#collapseCard-" + str(self.uuid) + "' class='d-block card-header py-3' data-toggle='collapse' role='button' aria-expanded='false' aria-controls='collapseCardExample'>"
        html_str += "<h6 class='m-0 font-weight-bold text-primary'>" + self.title + "</h6>\n"
        html_str += "Confidentiality: " + self.confidentiality_impact.adjusted_impact_level + " "
        html_str += "Availability: " + self.availability_impact.adjusted_impact_level + " "
        html_str += "Integrity: " + self.integrity_impact.adjusted_impact_level + " "
        html_str += "</a>\n"
        html_str += "<!-- Card Content - Collapse -->\n"
        html_str += "<div class='collapse' id='collapseCard-" + str(self.uuid) + "' aria-expanded='false' style=''>\n"
        html_str += "<div class='card-body'>\n"
        html_str += "Confidentiality: " + self.confidentiality_impact.__str__() + "<br>\n"
        html_str += "Availability: " + self.availability_impact.__str__() + "<br>\n"
        html_str += "Integrity: " + self.integrity_impact.__str__() + "<br>\n"
        html_str += self.description
        html_str += "\n</div>\n"
        html_str += "</div>\n"
        html_str += "</div>\n"
        return html_str

    def import_oscal(self, oscal_data,logger=None):
        oscal_data = self.fix_field_names(oscal_data)
        if "uuid" in oscal_data.keys():
            # check to see if the information_type already exists.  If not, create it
            try:
                obj = self._meta.model.objects.get(uuid=self.uuid)
                obj.update(oscal_data)
            except self.DoesNotExist:
                obj = self
                obj.title = oscal_data["title"]
                obj.description = oscal_data["description"]
                if "props" in oscal_data.keys():
                    for item in oscal_data["props"]:
                        p = props.import_oscal(item)
                        obj.props.add(p)
                if "links" in oscal_data.keys():
                    for item in oscal_data["links"]:
                        l = props.import_oscal(item)
                        obj.props.add(l)
                impact_types = ["confidentiality_impact", "integrity_impact", "availability_impact"]
                for i in impact_types:
                    d = oscal_data[i]
                    m = information_type_impact_level()
                    impact = m.import_oscal(d)
                    obj.__setattr__(i, impact)
        obj.save()
        return obj


class systems_information(PrimitiveModel):
    """
    Contains details about all information types that are stored, processed, or transmitted by the system, such as privacy information, and those defined in NIST SP 800-60.
    """

    class Meta:
        verbose_name = "System Information"
        verbose_name_plural = "Systems Information"

    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    information_types = CustomManyToManyField(
        to=information_types, verbose_name="Information Type",
        help_text="Contains details about one information type that is stored, processed, or transmitted by the system, such as privacy information, and those defined in NIST SP 800-60."
        )


# class system_status(BasicModel):
#     """
#     Describes the operational status of the system. If 'other' is selected, a remark must be included to describe the current state.
#     """
#
#     state_choices = [
#         ("operational", "Operational: The system is currently operating in production."),
#         ("under-development", "Under Development: The system is being designed, developed, or implemented"),
#         ("under-major-modification",
#          "Under Major Modification: The system is undergoing a major change, development, or transition."),
#         ("disposition", "Disposition: The system is no longer operational."),
#         ("other", "Other: Some other state, a remark must be included to describe the current state.")
#         ]
#
#     class Meta:
#         verbose_name = "System Status"
#         verbose_name_plural = "System Statuses"
#
#     state = ShortTextField(verbose_name="State", help_text="The current operating status.", choices=state_choices)


class diagrams(BasicModel):
    """
    A graphic that provides a visual representation the system, or some aspect of it.
    A diagram must include a link with a rel value of "diagram", who's href references a remote URI or an internal reference within this document containing the diagram.
    """

    class Meta:
        verbose_name = "Diagram"
        verbose_name_plural = "Diagrams"

    description = models.TextField(
        verbose_name="Diagram Description",
        help_text="A summary of the diagram. This description is intended to be used as alternate text to support compliance with requirements from Section 508 of the United States Workforce Rehabilitation Act of 1973.",
        blank=True
        )
    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    caption = ShortTextField(verbose_name="Caption", help_text="A brief caption to annotate the diagram.")


class authorization_boundaries(BasicModel):
    """
    A description of this system's authorization boundary, optionally supplemented by diagrams that illustrate the authorization boundary.
    """

    class Meta:
        verbose_name = "Authorization Boundary"
        verbose_name_plural = "Authorization Boundaries"

    description = models.TextField(
        verbose_name="Authorization Boundary Description",
        help_text="A summary of the system's authorization boundary."
        )
    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    diagrams = CustomManyToManyField(
        to=diagrams, verbose_name="Diagram(s)",
        help_text="A graphic that provides a visual representation the Authorization Boundary, or some aspect of it."
        )


class network_architectures(BasicModel):
    """
    A description of this system's Network Architecture, optionally supplemented by diagrams that illustrate the Network Architecture.
    """

    class Meta:
        verbose_name = "Network Architecture"
        verbose_name_plural = "Network Architectures"

    description = models.TextField(
        verbose_name="Network Architecture Description",
        help_text="A summary of the system's Network Architecture."
        )
    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    diagrams = CustomManyToManyField(
        to=diagrams, verbose_name="Diagram(s)",
        help_text="A graphic that provides a visual representation the Network Architecture, or some aspect of it."
        )


class data_flows(BasicModel):
    """
    A description of this system's data flow, optionally supplemented by diagrams that illustrate the data flow.
    """

    class Meta:
        verbose_name = "Data Flow"
        verbose_name_plural = "Data Flows"

    description = models.TextField(
        verbose_name="Data Flow Description",
        help_text="A summary of the system's Data Flow."
        )
    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    diagrams = CustomManyToManyField(
        to=diagrams, verbose_name="Diagram(s)",
        help_text="A graphic that provides a visual representation the Data Flow, or some aspect of it."
        )


class system_characteristics(BasicModel):
    """
    Contains the characteristics of the system, such as its name, purpose, and security impact level.
    """

    class Meta:
        verbose_name = "System Characteristics"
        verbose_name_plural = "Systems Characteristics"

    system_ids = CustomManyToManyField(
        to=system_ids, verbose_name="Alternative System Identifier",
        help_text="One or more unique identifier(s) for the system described by this system security plan."
        )
    system_name = ShortTextField(verbose_name="System Name - Full", help_text="The full name of the system.")
    system_name_short = ShortTextField(
        verbose_name="System Name - Short",
        help_text="A short name for the system, such as an acronym, that is suitable for display in a data table or summary list.",
        null=True
        )
    description = models.TextField(verbose_name="System Description", help_text="A summary of the system.", null=True)
    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    date_authorized = models.DateField(
        verbose_name="System Authorization Date",
        help_text="The date the system received its authorization.", null=True
        )
    security_sensitivity_level = ShortTextField(
        verbose_name="Security Sensitivity Level",
        help_text="The overall information system sensitivity categorization, such as defined by FIPS-199.", null=True
        )
    system_information = CustomManyToManyField(
        to=systems_information, verbose_name="System Information",
        help_text="Contains details about all information types that are stored, processed, or transmitted by the system, such as privacy information, and those defined in NIST SP 800-60."
        )
    security_impact_level = ShortTextField(
        verbose_name="Security Impact Level",
        help_text="The overall level of expected impact resulting from unauthorized disclosure, modification, or loss of access to information.",
        null=True
        )
    security_objective_confidentiality = ShortTextField(
        verbose_name="Security Objective: Confidentiality",
        help_text="A target-level of confidentiality for the system, based on the sensitivity of information within the system.",
        null=True
        )
    security_objective_integrity = ShortTextField(
        verbose_name="Security Objective: Integrity",
        help_text="A target-level of integrity for the system, based on the sensitivity of information within the system.",
        null=True
        )
    security_objective_availability = ShortTextField(
        verbose_name="Security Objective: Availability",
        help_text="A target-level of availability for the system, based on the sensitivity of information within the system.",
        null=True
        )
    status = ShortTextField(verbose_name="Status",
        help_text="Describes the operational status of the system.",null=True,choices=system_status_state_choices
        )
    authorization_boundary = models.ForeignKey(
        to=authorization_boundaries, verbose_name="Authorization Boundary",
        help_text="A description of this system's authorization boundary, optionally supplemented by diagrams that illustrate the authorization boundary.",
        on_delete=models.CASCADE, null=True
        )
    network_architecture = models.ForeignKey(
        to=network_architectures, verbose_name="Network Architecture",
        help_text="A description of the system's network architecture, optionally supplemented by diagrams that illustrate the network architecture.",
        on_delete=models.CASCADE, null=True
        )
    data_flow = models.ForeignKey(
        to=data_flows, verbose_name="Data Flow",
        help_text="A description of the system's data flow, optionally supplemented by diagrams that illustrate the data flow.",
        on_delete=models.CASCADE, null=True
        )
    responsible_parties = CustomManyToManyField(
        to=responsible_parties, verbose_name="Responsible Parties",
        help_text="A reference to a set of organizations or persons that have responsibility for performing a referenced role in the context of the containing object."
        )

    def __str__(self):
        return self.system_name


class leveraged_authorizations(BasicModel):
    """
    A description of another authorized system from which this system inherits capabilities that satisfy security requirements. Another term for this concept is a common control provider.
    """

    class Meta:
        verbose_name = "Authorization"
        verbose_name_plural = "Authorizations"

    title = ShortTextField(
        verbose_name="Title",
        help_text="A human readable name for the leveraged authorization in the context of the system."
        )
    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    party_uuid = models.ForeignKey(
        to=parties, verbose_name="Responsible Party",
        help_text="A reference to the party that manages the leveraged system.",
        on_delete=models.CASCADE
        )
    date_authorized = models.DateField(
        verbose_name="System Authorization Date",
        help_text="The date the system received its authorization."
        )

    def __str__(self):
        return self.title

class system_functions(PrimitiveModel):
    class Meta:
        verbose_name = "Function"
        verbose_name_plural = "Functions"

    system_functions = ShortTextField(
        verbose_name="Function",
        help_text="Describes a function performed for a given authorized privilege by this user class."
        )

    def __str__(self):
        return self.system_functions

class privileges(BasicModel):
    """
    Identifies a specific system privilege held by the user, along with an associated description and/or rationale for the privilege.
    """

    class Meta:
        verbose_name = "Privilege"
        verbose_name_plural = "Privileges"

    title = ShortTextField(
        verbose_name="User Title",
        help_text="A name given to the user, which may be used by a tool for display and navigation."
        )
    description = models.TextField(
        verbose_name="User Description",
        help_text=" A summary of the user's purpose within the system."
        )
    functions_performed = CustomManyToManyField(
        to=system_functions, verbose_name="Functions Performed",
        help_text="Describes a function performed for a given authorized privilege by this user class."
        )

    def __str__(self):
        return self.title


class users(BasicModel):
    """
    A type of user that interacts with the system based on an associated role.
    """

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    title = ShortTextField(
        verbose_name="User Title",
        help_text="A name given to the user, which may be used by a tool for display and navigation."
        )
    short_name = ShortTextField(
        verbose_name="User Short Name",
        help_text="A short common name, abbreviation, or acronym for the user."
        )
    description = models.TextField(
        verbose_name="User Description",
        help_text=" A summary of the user's purpose within the system."
        )
    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    role_ids = CustomManyToManyField(
        to=roles, verbose_name="User Role(s)",
        help_text="A reference to the roles served by the user."
        )
    authorized_privileges = CustomManyToManyField(
        to=privileges, verbose_name="Privilege",
        help_text="Identifies a specific system privilege held by the user, along with an associated description and/or rationale for the privilege."
        )

    def __str__(self):
        return self.title


class responsible_roles(BasicModel):
    """
    A reference to one or more roles with responsibility for performing a function relative to the containing object.
    """

    class Meta:
        verbose_name = "Responsible Role"
        verbose_name_plural = "Responsible Roles"

    role_id = models.ForeignKey(
        to=roles, verbose_name="Role",
        help_text="The role that is responsible for the business function.",
        on_delete=models.CASCADE
        )
    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    party_uuids = CustomManyToManyField(
        to=parties, verbose_name="Party Reference",
        help_text="References a party defined in metadata."
        )


class components(BasicModel):
    """
    A defined component that can be part of an implemented system. Components may be products, services, application programming interface (APIs), policies, processes, plans, guidance, standards, or other tangible items that enable security and/or privacy.
    """

    class Meta:
        verbose_name = "Component"
        verbose_name_plural = "Components"

    component_types = [
        ("this-system: The system as a whole.", 1),
        ("system: An external system, which may be a leveraged system or the other side of an interconnection.", 2),
        ("interconnection: A connection to something outside this system.", 3),
        ("software: Any software, operating system, or firmware.", 4),
        ("hardware: A physical device.", 5),
        ("service: A service that may provide APIs.", 6),
        ("policy: An enforceable policy.", 7),
        ("physical: A tangible asset used to provide physical protections or countermeasures.", 8),
        ("process-procedure: A list of steps or actions to take to achieve some end result.", 9),
        ("plan: An applicable plan.", 10),
        ("guidance: Any guideline or recommendation.", 11),
        ("standard: Any organizational or industry standard.", 12),
        (
            "validation: An external assessment performed on some other component, that has been validated by a third-party.",
            13),
        ("network: A physical or virtual network.", 14)
        ]

    type = ShortTextField(
        verbose_name="Component Type",
        help_text="A category describing the purpose of the component.", choices=component_types
        )
    title = ShortTextField(verbose_name="Component Title", help_text="A human readable name for the system component.")
    description = ShortTextField(
        verbose_name="Component Description",
        help_text="A description of the component, including information about its function."
        )
    purpose = ShortTextField(
        verbose_name="Purpose",
        help_text="A summary of the technological or business purpose of the component."
        )
    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    status = ShortTextField(verbose_name="Status",
        help_text=" Describes the operational status of the system component.",choices=system_status_state_choices
        )
    responsible_roles = CustomManyToManyField(
        to=responsible_roles, verbose_name="Responsible Roles",
        help_text="A reference to one or more roles with responsibility for performing a function relative to the containing object."
        )

    def __str__(self):
        return self.title


class inventory_items(BasicModel):
    """
    A set of inventory-item entries that represent the managed inventory instances of the system.
    """

    class Meta:
        verbose_name = "Inventory Item"
        verbose_name_plural = "Inventory Items"

    description = models.TextField(
        verbose_name="Inventory Item Description",
        help_text="A summary of the inventory item stating its purpose within the system."
        )
    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    responsible_parties = CustomManyToManyField(
        to=responsible_parties, verbose_name="Responsible Parties",
        help_text="A reference to a set of organizations or persons that have responsibility for performing a referenced role in the context of the containing object."
        )
    implemented_components = CustomManyToManyField(
        to=components, verbose_name="Implemented Components",
        help_text="The set of components that are implemented in a given system inventory item."
        )


class system_implementations(BasicModel):
    """
    Provides information as to how the system is implemented.
    """

    class Meta:
        verbose_name = "System Implementation"
        verbose_name_plural = "System Implementations"

    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    leveraged_authorizations = CustomManyToManyField(
        to=leveraged_authorizations,
        verbose_name="Leveraged Authorizations",
        help_text="A description of another authorized system from which this system inherits capabilities that satisfy security requirements. Another term for this concept is a common control provider."
        )
    users = CustomManyToManyField(
        to=users, verbose_name="System Users",
        help_text="A type of user that interacts with the system based on an associated role."
        )
    components = CustomManyToManyField(
        to=components, verbose_name="Components",
        help_text="A defined component that can be part of an implemented system. Components may be products, services, application programming interface (APIs), policies, processes, plans, guidance, standards, or other tangible items that enable security and/or privacy."
        )
    inventory_items = CustomManyToManyField(
        to=inventory_items, verbose_name="Inventory Items",
        help_text="A set of inventory-item entries that represent the managed inventory instances of the system."
        )


class parameters(BasicModel):
    """
    Identifies the parameter that will be set by the enclosed value.
    """

    class Meta:
        verbose_name = "Parameter"
        verbose_name_plural = "Parameters"

    param_id = ShortTextField(
        verbose_name="Parameter ID",
        help_text="A reference to a parameter within a control, who's catalog has been imported into the current implementation context."
        )
    values = ShortTextField(verbose_name="Parameter Value", help_text="A parameter value or set of values.")

    def __str__(self):
        return self.param_id + ": " + self.values

class implementation_status(BasicModel):
    """
    Describes the implementation status of the control. If 'Not-Applicable' is selected, a remark must be included to explain the justification.
    """

    state_choices = [
        ("Implemented: The control is fully implemented.", "implemented"),
        ("Partial: The control is partially implemented.", "partial"),
        ("Planned: There is a plan for implementing the control as explained in the remarks.", "planned"),
        ("Alternative: There is an alternative implementation for this control as explained in the remarks.",
         "alternative"),
        ("Not-Applicable: This control does not apply to this system as justified in the remarks.", "not-applicable")
        ]

    class Meta:
        verbose_name = "Implementation Status"
        verbose_name_plural = "Implementation Statuses"

    state = ShortTextField(
        verbose_name="State",
        help_text="Identifies the implementation status of the control or control objective.",
        choices=state_choices
        )


class provided_control_implementation(BasicModel):
    """
    Describes a capability which may be inherited by a leveraging system
    """

    class Meta:
        verbose_name = "Provided Control Implementation"
        verbose_name_plural = "Provided Control Implementations"

    description = models.TextField(
        verbose_name="Provided Control Implementation Description",
        help_text="An implementation statement that describes the aspects of the control or control statement implementation that can be provided to another system leveraging this system."
        )
    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    responsible_roles = CustomManyToManyField(
        to=responsible_roles, verbose_name="Responsible Roles",
        help_text="A reference to one or more roles with responsibility for performing a function relative to the containing object."
        )


class responsibilities(BasicModel):
    """
    Describes a control implementation responsibility imposed on a leveraging system.
    """

    class Meta:
        verbose_name = "Control Implementation Responsibility"
        verbose_name_plural = "Control Implementation Responsibilities"

    provided_uuid = models.ForeignKey(
        to=provided_control_implementation,
        verbose_name="Provided Control Implementation",
        help_text=" Identifies a 'provided' assembly associated with this assembly.",
        blank=True, on_delete=models.CASCADE
        )
    description = models.TextField(
        verbose_name="Control Implementation Responsibility Description",
        help_text="An implementation statement that describes the aspects of the control or control statement implementation that a leveraging system must implement to satisfy the control provided by a leveraged system."
        )
    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    responsible_roles = CustomManyToManyField(
        to=responsible_roles, verbose_name="Responsible Roles",
        help_text="A reference to one or more roles with responsibility for performing a function relative to the containing object."
        )


class export(BasicModel):
    """
    Identifies content intended for external consumption, such as with leveraged organizations.
    """

    class Meta:
        verbose_name = "Export"
        verbose_name_plural = "Exports"

    description = models.TextField(
        verbose_name="Control Implementation Export Description",
        help_text="An implementation statement that describes the aspects of the control or control statement implementation that can be available to another system leveraging this system."
        )
    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    provided = CustomManyToManyField(
        to=provided_control_implementation,
        verbose_name="Provided Control Implementations",
        help_text="Describes a capability which may be inherited by a leveraging system"
        )
    responsibilities = CustomManyToManyField(
        to=responsibilities, verbose_name="Control Implementation Responsibility",
        help_text="Describes a control implementation responsibility imposed on a leveraging system."
        )


class inherited(BasicModel):
    """
    Describes a control implementation responsibility inherited by a leveraging system.
    """

    class Meta:
        verbose_name = "Inherited Control Implementation"
        verbose_name_plural = "Inherited Control Implementations"

    provided_uuid = models.ForeignKey(
        to=provided_control_implementation,
        verbose_name="Provided Control Implementation",
        help_text=" Identifies a 'provided' assembly associated with this assembly.",
        blank=True, on_delete=models.CASCADE
        )
    description = models.TextField(
        verbose_name="Control Implementation Responsibility Description",
        help_text="An implementation statement that describes the aspects of a control or control statement implementation that a leveraging system is inheriting from a leveraged system."
        )
    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    responsible_roles = CustomManyToManyField(
        to=responsible_roles, verbose_name="Responsible Roles",
        help_text="A reference to one or more roles with responsibility for performing a function relative to the containing object."
        )


class satisfied(BasicModel):
    """
    Describes how this system satisfies a responsibility imposed by a leveraged system.
    """

    class Meta:
        verbose_name = "Satisfied Control Implementation Responsibility"
        verbose_name_plural = "Satisfied Control Implementation Responsibilities"

    responsibility_uuid = models.ForeignKey(
        to=responsibilities,
        verbose_name="Provided Control Implementation",
        help_text=" Identifies a 'provided' assembly associated with this assembly.",
        blank=True, on_delete=models.CASCADE
        )
    description = models.TextField(
        verbose_name="Control Implementation Responsibility Description",
        help_text="An implementation statement that describes the aspects of a control or control statement implementation that a leveraging system is inheriting from a leveraged system."
        )
    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    responsible_roles = CustomManyToManyField(
        to=responsible_roles, verbose_name="Responsible Roles",
        help_text="A reference to one or more roles with responsibility for performing a function relative to the containing object."
        )


class by_components(BasicModel):
    """
    Defines how the referenced component implements a set of controls.
    """

    class Meta:
        verbose_name = "Component Control Implementation"
        verbose_name_plural = "Component Control Implementations"

    component_uuid = CustomManyToManyField(
        to=components,
        verbose_name="Component Universally Unique Identifier Reference",
        help_text="A reference to the component that is implementing a given control or control statement."
        )
    description = models.TextField(
        verbose_name="Control Implementation Description",
        help_text="An implementation statement that describes how a control or a control statement is implemented within the referenced system component."
        )
    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    set_parameters = CustomManyToManyField(
        to=parameters, verbose_name="Set Parameter Value",
        help_text="Identifies the parameter that will be set by the enclosed value. Overrides globally set parameters of the same name"
        )
    implementation_status = CustomManyToManyField(
        to=implementation_status, verbose_name="Implementation Status",
        help_text="Indicates the degree to which the a given control is implemented."
        )
    export = models.ForeignKey(
        to=export, verbose_name="Export",
        help_text="Identifies content intended for external consumption, such as with leveraged organizations.",
        on_delete=models.CASCADE,null=True
        )
    inherited = CustomManyToManyField(
        to=inherited, verbose_name="Inherited Control Implementation",
        help_text="Describes a control implementation inherited by a leveraging system."
        )
    satisfied = CustomManyToManyField(
        to=satisfied, verbose_name="Satisfied Control Implementation Responsibility",
        help_text="Describes how this system satisfies a responsibility imposed by a leveraged system."
        )
    responsible_roles = CustomManyToManyField(
        to=responsible_roles, verbose_name="Responsible Roles",
        help_text="A reference to one or more roles with responsibility for performing a function relative to the containing object."
        )


class statements(BasicModel):
    """
    Identifies which statements within a control are addressed.
    """

    class Meta:
        verbose_name = "Statement"
        verbose_name_plural = "Statements"

    statement_id = ShortTextField(
        verbose_name="Control Statement Reference",
        help_text="A reference to a control statement by its identifier"
        )
    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    responsible_roles = CustomManyToManyField(
        to=responsible_roles, verbose_name="Responsible Role",
        help_text="A reference to one or more roles with responsibility for performing a function relative to the containing object."
        )
    by_components = CustomManyToManyField(
        to=by_components, verbose_name="Component Control Implementation",
        help_text="Defines how the referenced component implements a set of controls."
        )

    def __str__(self):
        return self.statement_id

class implemented_requirements(BasicModel):
    """
    Describes how the system satisfies an individual control.
    """

    class Meta:
        verbose_name = "Implemented Requirement"
        verbose_name_plural = "Implemented Requirements"

    control_id = ShortTextField(
        verbose_name="Control Identifier Reference",
        help_text="A reference to a control with a corresponding id value."
        )
    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    set_parameters = CustomManyToManyField(
        to=parameters, verbose_name="Set Parameter Value",
        help_text="Identifies the parameter that will be set by the enclosed value. Overrides globally set parameters of the same name"
        )
    responsible_roles = CustomManyToManyField(
        to=responsible_roles, verbose_name="Responsible Role",
        help_text="A reference to one or more roles with responsibility for performing a function relative to the containing object."
        )
    statements = CustomManyToManyField(
        to=statements, verbose_name="Specific Control Statement",
        help_text="Identifies which statements within a control are addressed."
        )
    by_components = CustomManyToManyField(
        to=by_components, verbose_name="Component Control Implementation",
        help_text="Defines how the referenced component implements a set of controls."
        )

    def __str__(self):
        try:
            c = controls.objects.get(control_id=self.control_id)
            r = c.title
        except ObjectDoesNotExist:
            r = self.control_id
        return r

class control_implementations(BasicModel):
    """
    Describes how the system satisfies a set of controls.
    """

    class Meta:
        verbose_name = "Control Implementation"
        verbose_name_plural = "Control Implementations"

    description = models.TextField(
        verbose_name="Description",
        help_text="Describes how the system satisfies a set of controls."
        )
    set_parameters = CustomManyToManyField(
        to=parameters, verbose_name="Common Parameters",
        help_text="Use of set-parameter in this context, sets the parameter for all related controls referenced in an implemented-requirement. If the same parameter is also set in a specific implemented-requirement, then the new value will override this value."
        )
    implemented_requirements = CustomManyToManyField(
        to=implemented_requirements,
        verbose_name="Control Based Requirements",
        help_text="Describes how the system satisfies controls."
        )

    def __str__(self):
        return self.description

class system_security_plans(BasicModel):
    """
    A system security plan, such as those described in NIST SP 800-18
    """

    class Meta:
        verbose_name = "System Security Plan (SSP)"
        verbose_name_plural = "System Security Plans (SSPs)"

    metadata = models.ForeignKey(to=metadata, on_delete=models.CASCADE)
    import_profile = models.ForeignKey(to=import_profiles, on_delete=models.CASCADE,null=True)
    system_characteristics = models.ForeignKey(to=system_characteristics, on_delete=models.CASCADE)
    system_implementation = models.ForeignKey(to=system_implementations, on_delete=models.CASCADE)
    control_implementation = models.ForeignKey(to=control_implementations, on_delete=models.CASCADE)
    back_matter = models.ForeignKey(
        to=back_matter, verbose_name="Back matter",
        help_text="Provides a collection of identified resource objects that can be referenced by a link with a rel value of 'reference' and an href value that is a fragment '#' followed by a reference to a reference identifier. Other specialized link 'rel' values also use this pattern when indicated in that context of use.",
        on_delete=models.CASCADE,null=True
        )

    def __str__(self):
        return self.metadata.title

    def to_html(self):
        html_str = "<h1>" + self.metadata.title + "</h1>"
        html_str += "<h2>Metadata</h2>"
        html_str += "<div class='card'  style=''>"
        html_str += "<div class='card-body'>"
        html_str += "<p class='card-text'>"
        if self.metadata is not None:
            html_str += self.metadata.to_html()
        html_str += "</p>"
        html_str += "</div>"
        html_str += "</div>"

        html_str += "<h2>System Characteristics</h2>"
        html_str += "<div class='card'  style=''>"
        html_str += "<div class='card-body'>"
        html_str += "<p class='card-text'>"
        if self.system_characteristics is not None:
            html_str += self.system_characteristics.to_html()
        html_str += "</p>"
        html_str += "</div>"
        html_str += "</div>"

        html_str += "<h2>System Implementation</h2>"
        html_str += "<div class='card'  style=''>"
        html_str += "<div class='card-body'>"
        html_str += "<p class='card-text'>"
        if self.system_implementation is not None:
            html_str += self.system_implementation.to_html()
        html_str += "</p>"
        html_str += "</div>"
        html_str += "</div>"

        html_str += "<h2>Control Implementation</h2>"
        html_str += "<div class='card'  style=''>"
        html_str += "<div class='card-body'>"
        html_str += "<p class='card-text'>"
        if self.control_implementation is not None:
            html_str += self.control_implementation.to_html()
        html_str += "</p>"
        html_str += "</div>"
        html_str += "</div>"

        html_str += "<h2>Back Matter</h2>"
        html_str += "<div class='card'  style=''>"
        html_str += "<div class='card-body'>"
        html_str += "<p class='card-text'>"
        if self.back_matter is not None:
            html_str += self.back_matter.to_html()
        html_str += "</p>"
        html_str += "</div>"
        html_str += "</div>"
        return html_str