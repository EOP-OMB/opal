from ckeditor.fields import RichTextField
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import reverse
from common.models import BasicModel, CustomManyToManyField, implementation_status_choices, parties, properties_field, links, roles, ShortTextField, system_status_state_choices, protocols
from catalog.models import controls, parts, params

import logging

logger = logging.getLogger('django')


# Create your models here.
class satisfied(BasicModel):
    """
    Describes how this system satisfies a responsibility imposed by a leveraged system.
    """

    class Meta:
        verbose_name = "Satisfied Control Implementation Responsibility"
        verbose_name_plural = "Satisfied Control Implementation Responsibilities"

    responsibility_uuid = models.ForeignKey(to="responsibilities", verbose_name="Provided Control Implementation", help_text=" Identifies a 'provided' assembly associated with this assembly.", blank=True, on_delete=models.CASCADE)
    description = RichTextField(
        verbose_name="Control Implementation Responsibility Description",
        help_text="An implementation statement that describes the aspects of a control or control statement implementation that a leveraging system is inheriting from a leveraged system."
        )
    props = properties_field()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    responsible_roles = CustomManyToManyField(to='responsible_roles', verbose_name="Responsible Roles", help_text="A reference to one or more roles with responsibility for performing a function relative to the containing object.")


class responsibilities(BasicModel):
    """
    Describes a control implementation responsibility imposed on a leveraging system.
    """

    class Meta:
        verbose_name = "Control Implementation Responsibility"
        verbose_name_plural = "Control Implementation Responsibilities"

    provided_uuid = models.ForeignKey(to="provided_control_implementation", verbose_name="Provided Control Implementation", help_text=" Identifies a 'provided' assembly associated with this assembly.", blank=True, on_delete=models.CASCADE)
    description = RichTextField(
        verbose_name="Control Implementation Responsibility Description",
        help_text="An implementation statement that describes the aspects of the control or control statement implementation that a leveraging system must implement to satisfy the control provided by a leveraged system."
        )
    props = properties_field()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    responsible_roles = CustomManyToManyField(to='responsible_roles', verbose_name="Responsible Roles", help_text="A reference to one or more roles with responsibility for performing a function relative to the containing object.")


class export(BasicModel):
    """
    Identifies content intended for external consumption, such as with leveraged organizations.
    """

    class Meta:
        verbose_name = "Export"
        verbose_name_plural = "Exports"

    description = RichTextField(
        verbose_name="Control Implementation Export Description",
        help_text="An implementation statement that describes the aspects of the control or control statement implementation that can be available to another system leveraging this system."
        )
    props = properties_field()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    provided = CustomManyToManyField(to="provided_control_implementation", verbose_name="Provided Control Implementations", help_text="Describes a capability which may be inherited by a leveraging system")
    responsibilities = CustomManyToManyField(to="responsibilities", verbose_name="Control Implementation Responsibility", help_text="Describes a control implementation responsibility imposed on a leveraging system.")


class inherited(BasicModel):
    """
    Describes a control implementation responsibility inherited by a leveraging system.
    """

    class Meta:
        verbose_name = "Inherited Control Implementation"
        verbose_name_plural = "Inherited Control Implementations"

    provided_uuid = models.ForeignKey(to="provided_control_implementation", verbose_name="Provided Control Implementation", help_text=" Identifies a 'provided' assembly associated with this assembly.", blank=True, on_delete=models.CASCADE)
    description = RichTextField(
        verbose_name="Control Implementation Responsibility Description",
        help_text="An implementation statement that describes the aspects of a control or control statement implementation that a leveraging system is inheriting from a leveraged system."
        )
    props = properties_field()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    responsible_roles = CustomManyToManyField(to='responsible_roles', verbose_name="Responsible Roles", help_text="A reference to one or more roles with responsibility for performing a function relative to the containing object.")


class responsible_roles(BasicModel):
    """
    A reference to one or more roles with responsibility for performing a function relative to the containing object.
    """

    class Meta:
        verbose_name = "Responsible Role"
        verbose_name_plural = "Responsible Roles"

    role_id = models.ForeignKey(to=roles, verbose_name="Role", help_text="The role that is responsible for the business function.", on_delete=models.CASCADE)
    props = properties_field()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    party_uuids = CustomManyToManyField(to=parties, verbose_name="Party Reference", help_text="References a party defined in metadata.")

    def __str__(self):
        return self.role_id.title


class parameters(BasicModel):
    """
    Sets the vale of a parameter for a specific implemented requirement.
    """

    class Meta:
        verbose_name = "Parameter"
        verbose_name_plural = "Parameters"

    param_id = models.ForeignKey(to=params, verbose_name="Parameter", help_text="A reference to a parameter within a control, who's catalog has been imported into the current implementation context.", on_delete=models.CASCADE)
    values = ShortTextField(verbose_name="Parameter Value", help_text="A parameter value or set of values.")
    by_component = models.ForeignKey(to='by_components', on_delete=models.CASCADE)

    def __str__(self):
        return self.param_id.param_id + ": " + self.values


class statements(BasicModel):
    """
    Identifies which statements within a control are addressed.
    """

    class Meta:
        verbose_name = "Statement"
        verbose_name_plural = "Statements"

    statement_id = CustomManyToManyField(to=parts, verbose_name="Control Statement Reference", help_text="A reference to a control statement by its identifier")
    props = properties_field()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    responsible_roles = CustomManyToManyField(to='responsible_roles', verbose_name="Responsible Role", help_text="A reference to one or more roles with responsibility for performing a function relative to the containing object.")
    by_components = CustomManyToManyField(to="by_components", verbose_name="Component Control Implementation", help_text="Defines how the referenced component implements a set of controls.")
    implemented_requirement = models.ForeignKey(to='implemented_requirements', on_delete=models.CASCADE)

    # def __str__(self):  # return self.statement_id.part_id


class by_components(BasicModel):
    """
    Defines how the referenced component implements a set of controls.
    """

    class Meta:
        verbose_name = "Component Control Implementation"
        verbose_name_plural = "Component Control Implementations"

    component_uuid = models.ForeignKey(to="components", verbose_name="Component Universally Unique Identifier Reference", help_text="A reference to the component that is implementing a given control or control statement.", on_delete=models.CASCADE)
    description = RichTextField(verbose_name="Control Implementation Description", help_text="An implementation statement that describes how a control or a control statement is implemented within the referenced system component.")
    props = properties_field()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    set_parameters = CustomManyToManyField(to=parameters, verbose_name="Set Parameter Value", help_text="Identifies the parameter that will be set by the enclosed value. Overrides globally set parameters of the same name")
    implementation_status = ShortTextField(verbose_name="Implementation Status", help_text="Indicates the degree to which the a given control is implemented.", choices=implementation_status_choices)
    export = models.ForeignKey(to="export", verbose_name="Export", help_text="Identifies content intended for external consumption, such as with leveraged organizations.", on_delete=models.CASCADE, null=True)
    inherited = CustomManyToManyField(to="inherited", verbose_name="Inherited Control Implementation", help_text="Describes a control implementation inherited by a leveraging system.")
    satisfied = CustomManyToManyField(to="satisfied", verbose_name="Satisfied Control Implementation Responsibility", help_text="Describes how this system satisfies a responsibility imposed by a leveraged system.")
    responsible_roles = CustomManyToManyField(to=responsible_roles, verbose_name="Responsible Roles", help_text="A reference to one or more roles with responsibility for performing a function relative to the containing object.")
    implemented_requirement = models.ForeignKey(to='implemented_requirements', on_delete=models.CASCADE)

    def to_html(self, indent=0):
        html_str = "<div class='component_control_implementation'>"
        html_str += self.description
        html_str += "</div>"
        return html_str


class provided_control_implementation(BasicModel):
    """
    Describes a capability which may be inherited by a leveraging system
    """

    class Meta:
        verbose_name = "Provided Control Implementation"
        verbose_name_plural = "Provided Control Implementations"

    description = RichTextField(
        verbose_name="Provided Control Implementation Description", help_text="An implementation statement that describes the aspects of the control or control statement implementation that can be provided to another system leveraging this system."
        )
    props = properties_field()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    responsible_roles = CustomManyToManyField(to=responsible_roles, verbose_name="Responsible Roles", help_text="A reference to one or more roles with responsibility for performing a function relative to the containing object.")


class implemented_requirements(BasicModel):
    """
    Describes how the system satisfies an individual control.
    """

    class Meta:
        verbose_name = "Implemented Requirement"
        verbose_name_plural = "Implemented Requirements"

    control_id = models.ForeignKey(to=controls, verbose_name="Control Identifier Reference", help_text="A reference to a control with a corresponding id value.", on_delete=models.CASCADE)
    props = properties_field()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    set_parameters = CustomManyToManyField(to=parameters, verbose_name="Set Parameter Value", help_text="Identifies the parameter that will be set by the enclosed value. Overrides globally set parameters of the same name")
    responsible_roles = CustomManyToManyField(to=responsible_roles, verbose_name="Responsible Role", help_text="A reference to one or more roles with responsibility for performing a function relative to the containing object.")
    control_implementation = models.ForeignKey(to='control_implementations', on_delete=models.CASCADE)

    def __str__(self):
        try:
            c = controls.objects.get(control_id=self.control_id)
            r = c.title
        except ObjectDoesNotExist:
            r = self.control_id
        return str(r)

    def to_html(self, indent=0):
        html_str = "<div class='implemented_requirement'>"
        html_str += self.control_id.to_html()
        if self.set_parameters.count() > 0:
            html_str += "<h4>Parameters</h4>"
            html_str += "<table>"
            html_str += "<tr><th>ID</th><th>Label</th><th>Guidelines</th><th>Value</th></tr>"
            for param in self.set_parameters.all():
                html_str += "<tr>"
                html_str += param.param_id.to_html()
                html_str += "<td>" + param.values + "</td>"
                html_str += "</tr>"
            html_str += "</table>"
        if self.by_components_set.count() > 0:
            html_str += "<h4>How is the control implemented?</h4>"
            for comp in self.by_components_set.all():
                html_str += comp.to_html()
        html_str += "</div>"
        return html_str


class control_implementations(BasicModel):
    """
    Describes how the system satisfies a set of controls.
    """

    class Meta:
        verbose_name = "Control Implementation"
        verbose_name_plural = "Control Implementations"

    description = RichTextField(verbose_name="Description", help_text="Describes how the system satisfies a set of controls.")
    set_parameters = CustomManyToManyField(
        to=parameters, verbose_name="Common Parameters",
        help_text="Use of set-parameter in this context, sets the parameter for all related controls referenced in an implemented-requirement. If the same parameter is also set in a specific implemented-requirement, then the new value will override this value."
        )
    component = models.ForeignKey(to='components', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.description

    def to_html(self,indent=0):
        html_str = "<div class='control_implementation'>"
        if len(self.description) > 0:
            html_str += "<h3>%s</h3>" % self.description
        if self.set_parameters.count() > 0:
            html_str += "Parameters defined by this Control Implementation:"
            html_str += "<table><tr><th>Parameter</th<th>Value</th></tr>"
            for param in self.set_parameters:
                html_str += "<tr><th>%s</th<th>%s</th></tr>" % (param.param_id, param.values)
            html_str += "</table>"
        if self.implemented_requirements_set.count() > 0:
            logger.info("getting implemented_requirements...")
            for imp_req in self.implemented_requirements_set.all():
                html_str += imp_req.to_html()
        html_str += "</div>"
        return html_str


class components(BasicModel):
    """
    A defined component that can be part of an implemented system. Components may be products, services, application
    programming interface (APIs), policies, processes, plans, guidance, standards, or other tangible items that enable
    security and/or privacy.
    """

    class Meta:
        verbose_name = "Component"
        verbose_name_plural = "Components"

    component_types = [("this-system", "This System: The system as a whole."), ("system", "Another System: An external system, which may be a leveraged system or the other side of an interconnection."),
                       ("interconnection", "System Interconnection: A connection to something outside this system."), ("software", "Software: Any software, operating system, or firmware."), ("hardware", "Hardware: A physical device."),
                       ("service", "Service: A service that may provide APIs."), ("policy", "Policy: An enforceable policy."), ("physical", "Physical: A tangible asset used to provide physical protections or countermeasures."),
                       ("process-procedure", "Process or Procedure: A list of steps or actions to take to achieve some end result."), ("plan", "Plan: An applicable plan."), ("guidance", "Guidance: Any guideline or recommendation."),
                       ("standard", "Standard: Any organizational or industry standard."), ("validation", "Validation: An external assessment performed on some other component, that has been validated by a third-party."),
                       ("network", "Network: A physical or virtual network.")]

    type = ShortTextField(verbose_name="Component Type", help_text="A category describing the purpose of the component.", choices=component_types)
    title = ShortTextField(verbose_name="Component Title", help_text="A human readable name for the system component.")
    description = RichTextField(verbose_name="Component Description", help_text="A description of the component, including information about its function.")
    purpose = ShortTextField(max_length=1000, verbose_name="Purpose", help_text="A summary of the technological or business purpose of the component.")
    props = properties_field()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    status = ShortTextField(verbose_name="Status", help_text=" Describes the operational status of the system component.", choices=system_status_state_choices)
    responsible_roles = CustomManyToManyField(to=responsible_roles, verbose_name="Responsible Roles", help_text="A reference to one or more roles with responsibility for performing a function relative to the containing object.")
    protocols = CustomManyToManyField(to=protocols, verbose_name="Service Protocol Information", help_text="Information about the protocol used to provide a service.")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('component:component_detail_view', kwargs={'pk': self.pk})

    def to_html(self,indent=0):
        html_str = ""
        html_str += "<h1>" + self.title + "</h1>"
        html_str += "<div>%s</div>" % self.description
        html_str += "<div>Purpose: %s</div>" % self.purpose
        html_str += "<div>Type: %s</div>" % self.type
        html_str += "<div class='container' style='margin-left: 0; margin-right: 0; background-color: greenyellow;'><div class='row justify-content-start'>"
        html_str += "<div class='col-sm-10' style='text-align: start;'><h2>Implemented Controls</h2></div>"
        html_str += "<div class='col-sm-2' style='text-align: end;'><h4><a href='%s'>Edit</a></h4></div>" % reverse('admin:component_components_change', args=(self.id,))
        html_str += "</div></div>"
        for imp in self.control_implementations_set.all():
            html_str += str(imp.to_html())
        return html_str
