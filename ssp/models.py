from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse

from catalog.models import controls
from ctrl_profile.models import ctrl_profiles
from component.models import components, responsible_roles, control_implementations, parameters
from common.models import BasicModel, PrimitiveModel, properties_field, props, ShortTextField, links, system_status_state_choices, responsible_parties, parties, roles, metadata, back_matter


class import_profiles(BasicModel):
    """
    Used to import the OSCAL profiles representing the system's control baseline.
    """

    class Meta:
        verbose_name = "Import Profile"
        verbose_name_plural = "Import Profiles"

    href = ShortTextField(verbose_name="Profile Reference", help_text="A resolvable URL reference to the profiles to use as the system's control baseline.", blank=True)
    local_profile = models.ForeignKey(to=ctrl_profiles, verbose_name="Profile Reference", help_text="A local profile to use as the system's control baseline.", null=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.local_profile is not None:
            s = self.local_profile.__str__()
        else:
            s = self.href
        return s


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

    def import_oscal(self, oscal_data):
        if type(oscal_data) is dict:
            if "identifier_type" in oscal_data.keys():
                self.identifier_type = \
                oscal_data[
                    "identifier_type"]
            if "system_id" in oscal_data.keys():
                self.system_id = \
                oscal_data[
                    "system_id"]
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

    def import_oscal(self, oscal_data):
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
    information_type_ids = models.ManyToManyField(
        to=information_type_ids, verbose_name="Information Type Systematized Identifier",
        help_text="An identifier qualified by the given identification system used, such as NIST SP 800-60."
    )


class information_type_impact_level(BasicModel):
    """
    The base and adjusted security impact level of a specific requirement (Confidentiality, Accessibility, or Integrity) for a specific information type on a specific information system
    """

    class Meta:
        verbose_name = "Information Type Impact Level"
        verbose_name_plural = "Information Type Impact Levels"

    props = properties_field()
    links = models.ManyToManyField(to=links, blank=True, verbose_name="Links")
    base = ShortTextField(
        verbose_name="Base Level (Confidentiality, Integrity, or Availability)",
        help_text="The prescribed base (Confidentiality, Integrity, or Availability) security impact level."
    )
    selected = ShortTextField(
        verbose_name="Selected Level (Confidentiality, Integrity, or Availability)",
        help_text="The selected (Confidentiality, Integrity, or Availability) security impact level.", null=True
    )
    adjustment_justification = RichTextField(
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

    def import_oscal(self, oscal_data):
        if type(oscal_data) is str:
            self.base = oscal_data
            self.save()
            return self
        else:
            oscal_data = self.convert_field_names_from_oscal_to_db(oscal_data)
            base = \
            oscal_data[
                "base"]
            if "selected" in oscal_data.keys():
                selected = \
                oscal_data[
                    "selected"]
            else:
                selected = None
            if "adjustment_justification" in oscal_data.keys():
                adjustment_justification = \
                oscal_data[
                    "adjustment_justification"]
            else:
                adjustment_justification = None
            obj, _ = self._meta.model.objects.get_or_create(
                base=base, selected=selected, adjustment_justification=adjustment_justification
            )
            if "props" in oscal_data.keys():
                for item in \
                oscal_data[
                    "props"]:
                    p = props.import_oscal(oscal_data=item)
                    obj.props.add(p)
            if "links" in oscal_data.keys():
                for item in \
                oscal_data[
                    "links"]:
                    l = props.import_oscal(oscal_data=item)
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
    categorizations = models.ManyToManyField(
        to=categorizations, verbose_name="Information Type Categorization",
        help_text="A set of information type identifiers qualified by the given identification system used, such as NIST SP 800-60."
    )
    props = properties_field()
    links = models.ManyToManyField(to=links, blank=True, verbose_name="Links")
    confidentiality_impact = models.ForeignKey(
        to=information_type_impact_level, verbose_name="Confidentiality Impact Level",
        help_text="The expected level of impact resulting from the unauthorized disclosure of the described information.",
        on_delete=models.CASCADE, related_name="confidentiality_impact"
    )
    integrity_impact = models.ForeignKey(
        to=information_type_impact_level, verbose_name="Integrity Impact Level",
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

    def to_html(self, indent=0, lazy=False):

        html_str = "<div class='card shadow mb-4'>\n"
        html_str += "<!-- Card Header - Accordion -->\n"
        html_str += "<a href='#collapseCard-" + str(
            self.uuid
        ) + "' class='d-block card-header py-3' data-toggle='collapse' role='button' aria-expanded='false' aria-controls='collapseCardExample'>"
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

    def import_oscal(self, oscal_data):
        oscal_data = self.convert_field_names_from_oscal_to_db(oscal_data)
        if "uuid" in oscal_data.keys():
            # check to see if the information_type already exists.  If not, create it
            try:
                obj = self._meta.model.objects.get(uuid=self.uuid)
                obj.update(oscal_data)
            except self.DoesNotExist:
                obj = self
                obj.title = \
                oscal_data[
                    "title"]
                obj.description = \
                oscal_data[
                    "description"]
                if "props" in oscal_data.keys():
                    for item in \
                    oscal_data[
                        "props"]:
                        p = props.import_oscal(oscal_data=item)
                        obj.props.add(p)
                if "links" in oscal_data.keys():
                    for item in \
                    oscal_data[
                        "links"]:
                        l = props.import_oscal(oscal_data=item)
                        obj.props.add(l)
                impact_types = [
                    "confidentiality_impact",
                    "integrity_impact",
                    "availability_impact"]
                for i in impact_types:
                    d = \
                    oscal_data[
                        i]
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

    props = properties_field()
    links = models.ManyToManyField(to=links, blank=True, verbose_name="Links")
    information_types = models.ManyToManyField(
        to=information_types, verbose_name="Information Type",
        help_text="Contains details about one information type that is stored, processed, or transmitted by the system, such as privacy information, and those defined in NIST SP 800-60."
    )

    def __str__(self):
        info_type_list = []
        for i in self.information_types.all():
            info_type_list.append(i.__str__())
        return ', '.join(info_type_list)


class diagrams(BasicModel):
    """
    A graphic that provides a visual representation the system, or some aspect of it.
    A diagram must include a link with a rel value of "diagram", who's href references a remote URI or an internal reference within this document containing the diagram.
    """

    class Meta:
        verbose_name = "Diagram"
        verbose_name_plural = "Diagrams"

    description = RichTextField(
        verbose_name="Diagram Description",
        help_text="A summary of the diagram. This description is intended to be used as alternate text to support compliance with requirements from Section 508 of the United States Workforce Rehabilitation Act of 1973.",
        blank=True
    )
    props = properties_field()
    links = models.ManyToManyField(to=links, blank=True, verbose_name="Links")
    caption = ShortTextField(verbose_name="Caption", help_text="A brief caption to annotate the diagram.")


class authorization_boundaries(BasicModel):
    """
    A description of this system's authorization boundary, optionally supplemented by diagrams that illustrate the authorization boundary.
    """

    class Meta:
        verbose_name = "Authorization Boundary"
        verbose_name_plural = "Authorization Boundaries"

    description = RichTextField(
        verbose_name="Authorization Boundary Description", help_text="A summary of the system's authorization boundary."
    )
    props = properties_field()
    links = models.ManyToManyField(to=links, blank=True, verbose_name="Links")
    diagrams = models.ManyToManyField(
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

    description = RichTextField(
        verbose_name="Network Architecture Description", help_text="A summary of the system's Network Architecture."
    )
    props = properties_field()
    links = models.ManyToManyField(to=links, blank=True, verbose_name="Links")
    diagrams = models.ManyToManyField(
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

    description = RichTextField(
        verbose_name="Data Flow Description", help_text="A summary of the system's Data Flow."
    )
    props = properties_field()
    links = models.ManyToManyField(to=links, blank=True, verbose_name="Links")
    diagrams = models.ManyToManyField(
        to=diagrams, verbose_name="Diagram(s)",
        help_text="A graphic that provides a visual representation the Data Flow, or some aspect of it."
    )


security_sensitivity_level_choices = (
(
'HIGH',
'HIGH'),
(
'MODERATE',
'MODERATE'),
(
'LOW',
'LOW'))


class system_characteristics(BasicModel):
    """
    Contains the characteristics of the system, such as its name, purpose, and security impact level.
    """

    class Meta:
        verbose_name = "System Characteristics"
        verbose_name_plural = "Systems Characteristics"

    system_ids = models.ManyToManyField(
        to=system_ids, verbose_name="Alternative System Identifier",
        help_text="One or more unique identifier(s) for the system described by this system security plan."
    )
    system_name = ShortTextField(verbose_name="System Name - Full", help_text="The full name of the system.")
    system_name_short = ShortTextField(
        verbose_name="System Name - Short",
        help_text="A short name for the system, such as an acronym, that is suitable for display in a data table or summary list.",
        null=True
    )
    description = RichTextField(verbose_name="System Description", help_text="A summary of the system.", null=True)
    props = properties_field()
    links = models.ManyToManyField(to=links, blank=True, verbose_name="Links")
    date_authorized = models.DateField(
        verbose_name="System Authorization Date", help_text="The date the system received its authorization.", null=True
    )
    security_sensitivity_level = ShortTextField(
        verbose_name="Security Sensitivity Level",
        help_text="The overall information system sensitivity categorization, such as defined by FIPS-199.", null=True, choices=security_sensitivity_level_choices
    )
    system_information = models.ManyToManyField(
        to=systems_information, verbose_name="System Information",
        help_text="Contains details about all information types that are stored, processed, or transmitted by the system, such as privacy information, and those defined in NIST SP 800-60."
    )
    security_impact_level = ShortTextField(
        verbose_name="Security Impact Level",
        help_text="The overall level of expected impact resulting from unauthorized disclosure, modification, or loss of access to information.",
        null=True, choices=security_sensitivity_level_choices
    )
    security_objective_confidentiality = ShortTextField(
        verbose_name="Security Objective: Confidentiality",
        help_text="A target-level of confidentiality for the system, based on the sensitivity of information within the system.",
        null=True, choices=security_sensitivity_level_choices
    )
    security_objective_integrity = ShortTextField(
        verbose_name="Security Objective: Integrity",
        help_text="A target-level of integrity for the system, based on the sensitivity of information within the system.",
        null=True, choices=security_sensitivity_level_choices
    )
    security_objective_availability = ShortTextField(
        verbose_name="Security Objective: Availability",
        help_text="A target-level of availability for the system, based on the sensitivity of information within the system.",
        null=True, choices=security_sensitivity_level_choices
    )
    status = ShortTextField(
        verbose_name="Status", help_text="Describes the operational status of the system.", null=True,
        choices=system_status_state_choices
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
    responsible_parties = models.ManyToManyField(
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
    props = properties_field()
    links = models.ManyToManyField(to=links, blank=True, verbose_name="Links")
    party_uuid = models.ForeignKey(
        to=parties, verbose_name="Responsible Party",
        help_text="A reference to the party that manages the leveraged system.", on_delete=models.CASCADE
    )
    date_authorized = models.DateField(
        verbose_name="System Authorization Date", help_text="The date the system received its authorization."
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
    description = RichTextField(
        verbose_name="User Description", help_text=" A summary of the user's purpose within the system."
    )
    functions_performed = models.ManyToManyField(
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
        verbose_name="User Short Name", help_text="A short common name, abbreviation, or acronym for the user."
    )
    description = RichTextField(
        verbose_name="User Description", help_text=" A summary of the user's purpose within the system."
    )
    props = properties_field()
    links = models.ManyToManyField(to=links, blank=True, verbose_name="Links")
    role_ids = models.ManyToManyField(
        to=roles, verbose_name="User Role(s)", help_text="A reference to the roles served by the user."
    )
    authorized_privileges = models.ManyToManyField(
        to=privileges, verbose_name="Privilege",
        help_text="Identifies a specific system privilege held by the user, along with an associated description and/or rationale for the privilege."
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

    description = RichTextField(
        verbose_name="Inventory Item Description",
        help_text="A summary of the inventory item stating its purpose within the system."
    )
    props = properties_field()
    links = models.ManyToManyField(to=links, blank=True, verbose_name="Links")
    responsible_parties = models.ManyToManyField(
        to=responsible_parties, verbose_name="Responsible Parties",
        help_text="A reference to a set of organizations or persons that have responsibility for performing a referenced role in the context of the containing object."
    )
    implemented_components = models.ManyToManyField(
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

    props = properties_field()
    links = models.ManyToManyField(to=links, blank=True, verbose_name="Links")
    leveraged_authorizations = models.ManyToManyField(
        to=leveraged_authorizations, verbose_name="Leveraged Authorizations",
        help_text="A description of another authorized system from which this system inherits capabilities that satisfy security requirements. Another term for this concept is a common control provider."
    )
    users = models.ManyToManyField(
        to=users, verbose_name="System Users",
        help_text="A type of user that interacts with the system based on an associated role."
    )
    components = models.ManyToManyField(
        to=components, verbose_name="Components",
        help_text="A defined component that can be part of an implemented system. Components may be products, services, application programming interface (APIs), policies, processes, plans, guidance, standards, or other tangible items that enable security and/or privacy."
    )
    inventory_items = models.ManyToManyField(
        to=inventory_items, verbose_name="Inventory Items",
        help_text="A set of inventory-item entries that represent the managed inventory instances of the system."
    )

    def to_html(self, indent=0, lazy=True):
        html_str = "<div>"
        # components
        html_str += "<h2>Components</h2>\n<ul>"
        if self.components.count() == 0:
            html_str = "<li>None</li>\n"
        else:
            for cmp in self.components.all():
                html_str += "<li>%s</li>\n" % cmp.to_html(indent=indent,lazy=lazy)
        # Inventory items
        html_str += "</ul>\n<h2>Inventory</h2>\n<ul>"
        if self.inventory_items.count() == 0:
            html_str += "<li>None</li>\n"
        else:
            for cmp in self.inventory_items.all():
                html_str += "<li>%s</li>\n" % cmp.to_html(indent=indent,lazy=lazy)
        # Users
        html_str += "</ul>\n<h2>Users</h2>\n<ul>"
        if self.users.count() == 0:
            html_str += "<li>None</li>\n"
        else:
            for u in self.users.all():
                html_str += "<li>%s</li>\n" % u.to_html(indent=indent,lazy=lazy)
        html_str += "</ul></div>"
        return html_str


    def __str__(self):
        return self.remarks


class system_security_plans(BasicModel):
    """
    A system security plan, such as those described in NIST SP 800-18
    """

    class Meta:
        verbose_name = "System Security Plan (SSP)"
        verbose_name_plural = "System Security Plans (SSPs)"

    metadata = models.ForeignKey(to=metadata, on_delete=models.CASCADE)
    import_profile = models.ForeignKey(to=import_profiles, on_delete=models.CASCADE, null=True)
    system_characteristics = models.ForeignKey(to=system_characteristics, on_delete=models.CASCADE)
    system_implementation = models.ForeignKey(to=system_implementations, on_delete=models.CASCADE)
    control_implementation = models.ForeignKey(to=control_implementations, on_delete=models.CASCADE,null=True)
    back_matter = models.ForeignKey(
        to=back_matter, verbose_name="Back matter",
        help_text="Provides a collection of identified resource objects that can be referenced by a link with a rel value of 'reference' and an href value that is a fragment '#' followed by a reference to a reference identifier. Other specialized link 'rel' values also use this pattern when indicated in that context of use.",
        on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return self.metadata.title

    def get_absolute_url(self):
        return reverse('ssp:ssp_detail_view', kwargs={'pk': self.pk})

    def to_html(self, indent=0, lazy=False):
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
