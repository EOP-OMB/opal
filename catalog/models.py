from django.db import models
from django.urls import reverse

from common.functions import coalesce, search_for_uuid
from common.models import BasicModel, PrimitiveModel, properties_field, ShortTextField, links, metadata, back_matter


class available_catalog_list(BasicModel):
    """
    List of catalogs available for import on the homepage
    """

    class Meta:
        verbose_name = "Catalog Source"
        verbose_name_plural = "Catalog Sources"

    catalog_uuid = models.UUIDField(editable=True, unique=True,
                                    help_text="The UUID for this catalog. All catalogs MUST have a unique UUID which should be the same across multiple systems.")
    link = models.URLField(verbose_name="Link to Catalog",
                           help_text="A complete URL which returns valid OSCAL json text")
    name = ShortTextField(verbose_name="Catalog Title", help_text="Human readable name of the catalog.")

    def get_link(self):
        catalog_import_url = reverse('catalog:import_catalog_view', kwargs={'catalog_id': self.id})
        if catalogs.objects.filter(uuid=self.catalog_uuid).exists():
            r = ["<li><a href='", catalog_import_url, "'>", self.name, "</a> &#9989;</li>"]
        else:
            r = ["<li><a href='", catalog_import_url, "'>", self.name, "</a></li>"]
        return "".join(r)


class tests(BasicModel):
    """
    A test expression which is expected to be evaluated by a tool
    """

    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Tests"

    expression = ShortTextField(verbose_name="Constraint test",
                                help_text="A formal (executable) expression of a constraint")

    def __str__(self):
        return self.expression


class constraints(PrimitiveModel):
    """
    A formal or informal expression of a constraint or test
    """

    class Meta:
        verbose_name = "Constraint"
        verbose_name_plural = "Constraints"

    description = models.TextField(verbose_name="Constraint Description",
                                   help_text="A textual summary of the constraint to be applied.")
    tests = models.ManyToManyField(to=tests, verbose_name="Constraint Test",
                                   help_text="A test expression which is expected to be evaluated by a tool",
                                   blank=True)

    def __str__(self):
        return self.description


class guidelines(PrimitiveModel):
    """
    A prose statement that provides a recommendation for the use of a parameter.
    """

    class Meta:
        verbose_name = "Guideline"
        verbose_name_plural = "Guidelines"

    prose = models.TextField(verbose_name="Prose", help_text="Prose permits multiple paragraphs, lists, tables etc.")

    def __str__(self):
        return self.prose


class params(BasicModel):
    """
    Parameters provide a mechanism for the dynamic assignment of value(s) in a control.
    """

    class Meta:
        verbose_name = "Parameter"
        verbose_name_plural = "Parameters"
        ordering = [
            "param_id"]

    param_id = ShortTextField(verbose_name="Parameter Identifier",
                              help_text="A unique identifier for a specific parameter instance. This identifier's uniqueness is document scoped and is intended to be consistent for the same parameter across minor revisions of the document.")
    param_class = ShortTextField(verbose_name="Parameter Class",
                                 help_text="A textual label that provides a characterization of the parameter. A class can be used in validation rules to express extra constraints over named items of a specific class value.",
                                 blank=True)
    depends_on = models.ForeignKey(to="params", verbose_name="Depends on",
                                   help_text=" Another parameter invoking this one", on_delete=models.CASCADE,
                                   null=True)
    props = properties_field
    links = models.ManyToManyField(to=links, blank=True, verbose_name="Links")
    label = ShortTextField(verbose_name="Parameter Label",
                           help_text="A short, placeholder name for the parameter, which can be used as a substitute for a value if no value is assigned.")
    usage = models.TextField(verbose_name="Parameter Usage Description",
                             help_text="Describes the purpose and use of a parameter")
    constraints = models.ManyToManyField(to=constraints, verbose_name="Constraints",
                                         help_text="A formal or informal expression of a constraint or test",
                                         blank=True)
    guidelines = models.ManyToManyField(to=guidelines, blank=True, verbose_name="Guidelines",
                                        help_text="A prose statement that provides a recommendation for the use of a parameter.")
    values = ShortTextField(verbose_name="Values", help_text="An array of comma seperated value strings", blank=True)
    select = ShortTextField(verbose_name="Selection", help_text="Presenting a choice among alternatives", blank=True)
    how_many = ShortTextField(verbose_name="Parameter Cardinality",
                              help_text="Describes the number of selections that must occur. Without this setting, only one value should be assumed to be permitted.",
                              choices=[("one", "Only one value is permitted."),
                                       ("one-or-more", "One or more values are permitted.")])
    choice = models.TextField(verbose_name="Choices", help_text="A list of values. One value per line")

    def get_form(self):
        html_str = "<tr><td>"
        if self.guidelines.count() > 0:
            for guideline in self.guidelines.all():
                html_str += guideline.prose
        html_str += "</td><td>%s</td><td>" % self.param_id
        if self.select != '':
            # This should be a drop-down
            if self.how_many == "one-or-more":
                html_str += "<select multiple name='%s'>" % self.param_id
            else:
                html_str += "<select name='%s'>" % self.param_id
            choices = self.choice.split("\n")
            for option in choices:
                html_str += "<option>%s</option>" % option
            html_str += "</select>"
        else:
            html_str += "<input type=text value='%s' name='%s'>" % (self.values, self.param_id)
        html_str += "</td></tr>"
        return html_str

    def __str__(self):
        return "%s: %s" % (self.param_id, self.label)

    def field_name_changes(self):
        d = {"id": "param_id"}
        return d

    def to_html(self, indent=0, lazy=False):
        html_str = "<td>" + self.param_id + "</td>"
        html_str += "<td>" + self.label + "</td>"
        html_str += "<td>"
        if len(self.guidelines.all()) > 0:
            for g in self.guidelines.all():
                html_str += g.__str__()
            html_str += "</td>"
        return html_str


class parts(PrimitiveModel):
    """
    A part provides for logical partitioning of prose, and can be thought of as a grouping structure (e.g., section). A part can have child parts allowing for arbitrary nesting of prose content (e.g., statement hierarchy). A part can contain prop objects that allow for enriching prose text with structured name/value information.
    """

    class Meta:
        verbose_name = "Part"
        verbose_name_plural = "Parts"

    part_id = ShortTextField(
        verbose_name="Part Identifier",
        help_text="A unique identifier for a specific part instance. This identifier's uniqueness is document scoped and is intended to be consistent for the same part across minor revisions of the document.",
        blank=True
    )
    name = ShortTextField(verbose_name="Part Name",
                          help_text=" A textual label that uniquely identifies the part's semantic type.")
    ns = ShortTextField(verbose_name="Part Namespace",
                        help_text="A namespace qualifying the part's name. This allows different organizations to associate distinct semantics with the same name.",
                        blank=True)
    part_class = ShortTextField(
        verbose_name="Part Class",
        help_text="A textual label that provides a sub-type or characterization of the part's name. This can be used to further distinguish or discriminate between the semantics of multiple parts of the same control with the same name and ns.",
        blank=True
    )
    title = ShortTextField(verbose_name="Part Title",
                           help_text="A name given to the part, which may be used by a tool for display and navigation.",
                           blank=True)
    props = properties_field()
    prose = models.TextField(verbose_name="Part Text", help_text="Permits multiple paragraphs, lists, tables etc.")
    sub_parts = models.ManyToManyField(to="parts", blank=True, verbose_name="Sub Parts",
                                       help_text="A part can have child parts allowing for arbitrary nesting of prose content (e.g., statement hierarchy).")
    links = models.ManyToManyField(to=links, blank=True, verbose_name="Links")

    def to_html(self, indent=0, show_guidance=True, show_links=True, lazy=False):
        html_str = ""
        if self.name in ["item", "statement"]:
            if len(self.props.filter(name="label")) > 0:
                html_str += self.props.get(name="label").value + " "
            html_str += self.prose + "<br>\n"
        if self.name == "guidance" and show_guidance:
            html_str = "<h5>Guidance</h5>"
            html_str += "<p>" + self.prose + "</p>"
        if len(self.sub_parts.all()) > 0:
            indent += 2
            for p in self.sub_parts.all():
                html_str += "&nbsp;" * indent + p.to_html(indent=indent, show_guidance=show_guidance,
                                                          show_links=show_links)
        if len(self.links.all()) > 0 and show_links:
            html_str += "<hr>"
            for link in self.links.all():
                html_str += link.to_html() + "<br>"
        return html_str

    def get_root_part(self):
        if self.parts_set.first() is not None:
            parent_part = self.parts_set.first()
            root_prt = parent_part.get_root_part()
        else:
            root_prt = self
        return root_prt

    @property
    def get_control(self):
        root_prt = self.get_root_part()
        ctrl = root_prt.controls_set.first()
        return ctrl

    def __str__(self):
        if len(self.part_id) > 0:
            s = self.part_id
        elif len(self.title) > 0:
            s = self.title
        elif len(self.name) > 0:
            s = self.name
        elif len(self.prose) > 0:
            s = self.prose[0:100]
        else:
            s = "Part: %s" % str(self.uuid)
        return s

    def field_name_changes(self):
        d = {"id": "part_id", "class": "part_class", "parts": "sub_parts"}
        return d

    def get_all_parts(self):
        part_list = [self]
        if self.sub_parts.count() > 0:
            for part in self.sub_parts.all():
                part_list.extend(part.get_all_parts())
        return part_list


class controls(PrimitiveModel):
    """
    A structured information object representing a security or privacy control. Each security or privacy control within the Catalog is defined by a distinct control instance.
    """

    class Meta:
        verbose_name = "Control"
        verbose_name_plural = "Controls"
        ordering = ['sort_id']

    control_id = ShortTextField(
        verbose_name="Control Identifier",
        help_text="A unique identifier for a specific control instance that can be used to reference the control in other OSCAL documents. This identifier's uniqueness is document scoped and is intended to be consistent for the same control across minor revisions of the document."
    )
    control_class = ShortTextField(
        verbose_name="Control Class",
        help_text="A textual label that provides a sub-type or characterization of the control."
    )
    title = ShortTextField(
        verbose_name="Control Title",
        help_text=" A name given to the control, which may be used by a tool for display and navigation."
    )
    params = models.ManyToManyField(
        to=params, verbose_name="Control Parameters", blank=True,
        help_text="Parameters provide a mechanism for the dynamic assignment of value(s) in a control."
    )
    props = properties_field()
    links = models.ManyToManyField(to=links, blank=True, verbose_name="Links")
    parts = models.ManyToManyField(
        to=parts, verbose_name="Parts", help_text="A partition of a control's definition or a child of another part.",
        blank=True
    )
    control_enhancements = models.ManyToManyField(
        to="controls", verbose_name="Control Enhancements", help_text="Additional sub-controls", blank=True
    )
    sort_id = ShortTextField(max_length=25, verbose_name="Sort ID",
                             help_text="normalized value to sort controls in the correct order", null=True)

    @property
    def _get_sort_id(self):
        if self.props.filter(name='sort-id').exists():
            sort_id = self.props.get(name='sort-id').value
        else:
            sort_id = self.control_id.lower()
        return sort_id

    def set_sort_id(self):
        if self.sort_id is None:
            self.sort_id = self._get_sort_id
            return True
        return False

    def get_absolute_url(self):
        url = reverse('catalog:control_detail_view', args=[self.id])
        return url

    def get_all_parts(self):
        part_list = []
        for part in self.parts.all():
            part_list.extend(part.get_all_parts())
        return part_list

    def get_all_components(self):
        component_list = []
        if self.implemented_requirements_set.count() > 0:
            implemented_requirements_list = self.implemented_requirements_set.all()
            for i in implemented_requirements_list:
                if i.control_implementations_set.count() > 0:
                    control_implementations_list = i.control_implementations_set.all()
                    for control_implementation in control_implementations_list:
                        if control_implementation.component.title not in component_list:
                            component_list.append(control_implementation.component.title)
            component_list.sort()
            html_str = "<ul>"
            for comp in component_list:
                html_str += "<li>%s</li>" % comp
            html_str += "</ul>"
        else:
            html_str = "Control is not implemented."
        return html_str

    def __str__(self):
        return self.control_class + " " + self.control_id + " " + self.title

    def field_name_changes(self):
        d = {"id": "control_id", "class": "control_class", "controls": "control_enhancements"}
        return d

    def to_html(self, indent=0, lazy=False):
        self.set_sort_id()
        html_str = "<a id=" + self.control_id + ">"
        html_str += "<h4>"
        html_str += self.control_id.upper() + " - "
        html_str += self.title
        html_str += " (" + self.control_class + ")"
        html_str += "</h4>"
        if self.parts is not None:
            for i in self.parts.all():
                html_str += i.to_html()
        if self.params is not None:
            for i in self.params.all():
                str_to_replace = '{{ insert: param, ' + i.param_id + ' }}'
                html_str = html_str.replace(str_to_replace, '(<i>' + coalesce(i.select, i.label, i.param_id) + '</i>)')
        if self.links is not None:
            html_str += "<div><strong>Related Controls:</strong><br>"
            for i in self.links.filter(rel="related"):
                html_str += i.to_html() + '<br>'
            html_str += "</div>"

            reference_links = []
            for i in self.links.filter(rel="reference"):
                obj = search_for_uuid(i.href[1:])
                if obj is not None:
                    reference_links.append(obj.to_html())
            html_str += "<p><strong>References:</strong> "
            html_str += ", ".join(reference_links)
            html_str += "</p>"
        if self.control_enhancements is not None:
            for i in self.control_enhancements.all():
                html_str += i.to_html()
        return html_str

    def to_html_short(self):
        html_str = "<a id=" + self.control_id + ">"
        html_str += "<h4>"
        html_str += self.control_id.upper() + " - "
        html_str += self.title
        html_str += " (" + self.control_class + ")"
        html_str += "</h4>"
        if self.parts is not None:
            for i in self.parts.all():
                html_str += i.to_html(show_guidance=False, show_links=False)
        if self.params is not None:
            for i in self.params.all():
                str_to_replace = '{{ insert: param, ' + i.param_id + ' }}'
                html_str = html_str.replace(str_to_replace, '(<i>' + coalesce(i.select, i.label, i.param_id) + '</i>)')
        return html_str

    def count_controls(self):
        control_count = 1
        control_enhancement_count = 0
        if self.control_enhancements is not None:
            for i in self.control_enhancements.all():
                cc, cec = i.count_controls()
                control_enhancement_count += cc + cec
        return control_count, control_enhancement_count

    def list_all_controls(self):
        control_list = [self]
        if self.control_enhancements is not None:
            for i in self.control_enhancements.all():
                control_list.append(i)
        return control_list


class groups(PrimitiveModel):
    """
    A Group is an arbitrary collection of controls.  It cna contain other groups and controls
    """

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"
        ordering = ["group_id"]

    group_id = ShortTextField(
        verbose_name="Control Identifier",
        help_text="A unique identifier for a specific control instance that can be used to reference the control in other OSCAL documents. This identifier's uniqueness is document scoped and is intended to be consistent for the same control across minor revisions of the document."
    )
    group_class = ShortTextField(
        verbose_name="Group Class",
        help_text="A textual label that provides a sub-type or characterization of the control."
    )
    title = ShortTextField(
        verbose_name="Control Title",
        help_text=" A name given to the control, which may be used by a tool for display and navigation."
    )
    params = models.ManyToManyField(
        to=params, verbose_name="Global Group Parameters",
        help_text="Parameters that should be applied to all Controls in the Group", blank=True
    )
    props = properties_field(
        verbose_name="Global Group Properties",
        help_text="Properties that should be applied to all Controls in the Group"
    )
    links = models.ManyToManyField(to=links, blank=True, verbose_name="Links")
    parts = models.ManyToManyField(
        to=parts, verbose_name="Parts", help_text="A partition of a control's definition or a child of another part.",
        blank=True
    )
    sub_groups = models.ManyToManyField(
        to="groups", verbose_name="Sub Groups", help_text="A group of controls, or of groups of controls.", blank=True
    )
    controls = models.ManyToManyField(
        to="controls", blank=True, verbose_name="Controls",
        help_text="A structured information object representing a security or privacy control. Each security or privacy control within the Catalog is defined by a distinct control instance."
    )

    def get_absolute_url(self):
        return reverse('catalog:group_detail_view', kwargs={'pk': self.pk})

    def __str__(self):
        return self.group_id.upper() + " - " + self.title + " (" + self.group_class + ")"

    def field_name_changes(self):
        d = {"id": "group_id", "class": "group_class", "groups": "sub_groups"}
        return d

    def to_html(self, indent=0, lazy=False):
        html_str = "<h3>"
        html_str += self.group_id.upper() + " - "
        html_str += self.title
        html_str += " (" + self.group_class + ")"
        html_str += "</h3>"
        if self.props is not None:
            for i in self.props.all():
                html_str += i.to_html()
        if self.params is not None:
            for i in self.params.all():
                html_str += i.to_html()
        if self.links is not None:
            for i in self.links.all():
                html_str += i.to_html()
        if self.parts is not None:
            for i in self.parts.all():
                html_str += i.to_html()
        if self.sub_groups is not None:
            for i in self.sub_groups.all():
                html_str += i.to_html()
        if self.controls is not None:
            for i in self.controls.all():
                html_str += i.to_html()

        return html_str

    def count_controls(self):
        control_count = 0
        control_enhancement_count = 0
        if self.sub_groups is not None:
            for i in self.sub_groups.all():
                cc, cec = i.count_controls()
                control_count += cc
        if self.controls is not None:
            for i in self.controls.all():
                cc, cec = i.count_controls()
                control_count += cc
                control_enhancement_count += cec
        return control_count, control_enhancement_count

    def list_all_controls(self):
        control_list = []
        if self.sub_groups is not None:
            for i in self.sub_groups.all():
                control_list.extend(i.list_all_controls())
        if self.controls is not None:
            for i in self.controls.all():
                control_list.extend(i.list_all_controls())
        return control_list


class catalogs(PrimitiveModel):
    """
    A collection of controls.
    """

    class Meta:
        verbose_name = "Control Catalog"
        verbose_name_plural = "Control Catalogs"

    catalog_uuid = models.UUIDField(verbose_name="Catalog Universally Unique Identifier", null=True)
    metadata = models.ForeignKey(
        to=metadata, verbose_name="Publication metadata",
        help_text="Provides information about the publication and availability of the containing document.",
        on_delete=models.CASCADE
    )
    params = models.ManyToManyField(
        to=params, verbose_name="Global Catalog Parameters",
        help_text="Parameters that should be applied to all Controls in the Catalog", blank=True
    )
    controls = models.ManyToManyField(to=controls, verbose_name="Controls", blank=True)
    groups = models.ManyToManyField(to=groups, verbose_name="Groups", blank=True)
    back_matter = models.ForeignKey(to=back_matter, verbose_name="Back Matter", on_delete=models.CASCADE, null=True)

    def field_name_changes(self):
        """
        Returns a dictionary object that contains the internal field name as the key and the original name as the value
        """
        fields_to_rename = {'uuid': 'catalog_uuid', 'back-matter': 'back_matter'}
        return fields_to_rename

    @property
    def title(self):
        return self.metadata.title

    def __str__(self):
        return self.metadata.title

    def get_absolute_url(self):
        return reverse('catalog:catalog_detail_view', kwargs={'pk': self.pk})

    def to_html(self, indent=0, lazy=False):
        html_str = "<h1>" + self.metadata.title + "</h1>"
        html_str += "<h2>Metadata</h2>"
        html_str += self.metadata.to_html()
        html_str += "<hr>\n"
        if self.params is not None:
            html_str += "<h1>Global Parameters</h1>\n"
            for i in self.params.all():
                html_str += i.to_html()
        if self.groups is not None:
            html_str += "<h1>Groups</h1>\n"
            for i in self.groups.all():
                html_str += "<a href='%s'>%s</a><br>\n" % (i.get_absolute_url(), i.__str__())
        if self.controls is not None:
            html_str += "<h1>Controls not in a Group</h1>\n"
            for i in self.controls.all():
                html_str += i.to_html()
        if self.back_matter is not None:
            html_str += "<h1>Back Matter</h1>\n"
            html_str += self.back_matter.to_html()
        return html_str

    def count_controls(self):
        control_count = 0
        control_enhancement_count = 0
        control_count_total = 0
        html_str = "<th><a href='" + self.get_absolute_url() + "'>" + self.metadata.title + "</a></th>"
        if self.groups is not None:
            control_count_total_for_group = 0
            for i in self.groups.all():
                cc, cec = i.count_controls()
                control_count += cc
                control_enhancement_count += cec
                control_count_total_for_group += cc + cec
            control_count_total += control_count_total_for_group
        if self.controls is not None:
            control_count_total_for_group = 0
            for i in self.controls.all():
                cc, cec = i.count_controls()
                control_count += cc
                control_enhancement_count += cec
                control_count_total_for_group += cc + cec
            control_count_total += control_count_total_for_group
        html_str += "<td>%d</td>" % control_count
        html_str += "<td>%d</td>" % control_enhancement_count
        html_str += "<td>%d</td>" % control_count_total
        return html_str

    def list_all_controls(self):
        control_list = []
        if self.groups is not None:
            for i in self.groups.all():
                control_list.extend(i.list_all_controls())
        if self.controls is not None:
            for i in self.controls.all():
                control_list.extend(i.list_all_controls())
        return control_list
