from common.models import *


class tests(BasicModel):
    """
    A test expression which is expected to be evaluated by a tool
    """

    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Tests"

    expression = ShortTextField(
        verbose_name="Constraint test",
        help_text="A formal (executable) expression of a constraint"
        )

    def __str__(self):
        return self.expression


class constraints(PrimitiveModel):
    """
    A formal or informal expression of a constraint or test
    """

    class Meta:
        verbose_name = "Constraint"
        verbose_name_plural = "Constraints"

    description = models.TextField(
        verbose_name="Constraint Description",
        help_text="A textual summary of the constraint to be applied."
        )
    tests = CustomManyToManyField(
        to=tests, verbose_name="Constraint Test",
        help_text="A test expression which is expected to be evaluated by a tool"
        )

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

    param_id = ShortTextField(
        verbose_name="Parameter Identifier",
        help_text="A unique identifier for a specific parameter instance. This identifier's uniqueness is document scoped and is intended to be consistent for the same parameter across minor revisions of the document."
        )
    param_class = ShortTextField(
        verbose_name="Parameter Class",
        help_text="A textual label that provides a characterization of the parameter. A class can be used in validation rules to express extra constraints over named items of a specific class value.",
        blank=True
        )
    depends_on = models.ForeignKey(
        to="params", verbose_name="Depends on",
        help_text=" Another parameter invoking this one", on_delete=models.CASCADE, null=True
        )
    props = propertiesField
    links = CustomManyToManyField(to=links, verbose_name="Links")
    label = ShortTextField(
        verbose_name="Parameter Label",
        help_text="A short, placeholder name for the parameter, which can be used as a substitute for a value if no value is assigned."
        )
    usage = models.TextField(
        verbose_name="Parameter Usage Description",
        help_text="Describes the purpose and use of a parameter"
        )
    constraints = CustomManyToManyField(
        to=constraints, verbose_name="Constraints",
        help_text="A formal or informal expression of a constraint or test"
        )
    guidelines = CustomManyToManyField(
        to=guidelines, verbose_name="Guidelines",
        help_text="A prose statement that provides a recommendation for the use of a parameter."
        )
    values = ShortTextField(verbose_name="Values", help_text="An array of comma seperated value strings", blank=True)
    select = ShortTextField(verbose_name="Selection", help_text="Presenting a choice among alternatives", blank=True)
    how_many = ShortTextField(
        verbose_name="Parameter Cardinality",
        help_text="Describes the number of selections that must occur. Without this setting, only one value should be assumed to be permitted.",
        choices=[("one", "Only one value is permitted."),
                 ("one-or-more", "One or more values are permitted.")]
        )
    choice = models.TextField(verbose_name="Choices", help_text="A list of values. One value per line")

    def __str__(self):
        return self.param_id

    def field_name_changes(self):
        d = {"id": "param_id"}
        return d

    def to_html(self):
        html_str = "<td>" + self.param_id + "</td>"
        # html_str += "<td>" + coalesce(self.depends_on) + "</td>"
        html_str += "<td>" + self.label + "</td>"
        html_str += "<td>"
        if len(self.guidelines.all()) > 0:
            for g in self.guidelines.all():
                html_str += g.__str__()
            html_str += "</td>"
        # html_str += "<td>" + coalesce(self.usage) + "</td>"
        # html_str += "<td>" + coalesce(self.values) + "</td>"
        # html_str += "<td>" + coalesce(self.select) + "</td>"
        # html_str += "<td>" + coalesce(self.how_many) + "</td>"
        # html_str += "<td>" + coalesce(self.choice) + "</td>"
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
    name = ShortTextField(
        verbose_name="Part Name",
        help_text=" A textual label that uniquely identifies the part's semantic type."
        )
    ns = ShortTextField(
        verbose_name="Part Namespace",
        help_text="A namespace qualifying the part's name. This allows different organizations to associate distinct semantics with the same name.",
        blank=True
        )
    part_class = ShortTextField(
        verbose_name="Part Class",
        help_text="A textual label that provides a sub-type or characterization of the part's name. This can be used to further distinguish or discriminate between the semantics of multiple parts of the same control with the same name and ns.",
        blank=True
        )
    title = ShortTextField(
        verbose_name="Part Title",
        help_text="A name given to the part, which may be used by a tool for display and navigation.",
        blank=True
        )
    props = propertiesField()
    prose = MarkdownxField(verbose_name="Part Text", help_text="Permits multiple paragraphs, lists, tables etc.")
    sub_parts = CustomManyToManyField(
        to="parts", verbose_name="Sub Parts",
        help_text="A part can have child parts allowing for arbitrary nesting of prose content (e.g., statement hierarchy)."
        )
    links = CustomManyToManyField(to=links, verbose_name="Links")

    def to_html(self,indent=0):
        html_str = ""
        if self.name in ["item","statement"]:
            if len(self.props.filter(name="label")) > 0:
                html_str += self.props.get(name="label").value + " "
            html_str += self.prose + "<br>\n"
        if self.name == "guidance":
            html_str = "<h5>Guidance</h5>"
            html_str += "<p>" + self.prose + "</p>"
        if len(self.sub_parts.all()) > 0:
            indent += 2
            for p in self.sub_parts.all():
                html_str += "&nbsp;"*indent + p.to_html(indent=indent)
        if len(self.links.all()) > 0:
            html_str += "<hr>"
            for l in self.links.all():
                html_str += l.to_html() + "<br>"
        return html_str

    def __str__(self):
        if len(self.part_id) > 0:
            return self.part_id
        if len(self.title) > 0:
            return self.title
        elif len(self.name) > 0:
            return self.name
        elif len(self.prose) > 0:
            return self.prose[0:100]
        else:
            return "Part: " + str(self.uuid)

    def field_name_changes(self):
        d = {"id": "part_id", "class": "part_class", "parts": "sub_parts"}
        return d


class controls(PrimitiveModel):
    """
    A structured information object representing a security or privacy control. Each security or privacy control within the Catalog is defined by a distinct control instance.
    """

    class Meta:
        verbose_name = "Control"
        verbose_name_plural = "Controls"

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
    params = CustomManyToManyField(
        to=params, verbose_name="Control Parameters",
        help_text="Parameters provide a mechanism for the dynamic assignment of value(s) in a control."
        )
    props = propertiesField()
    links = CustomManyToManyField(to=links, verbose_name="Links")
    parts = CustomManyToManyField(
        to=parts, verbose_name="Parts",
        help_text="A partition of a control's definition or a child of another part."
        )
    control_enhancements = CustomManyToManyField(
        to="controls", verbose_name="Control Enhancements",
        help_text="Additional sub-controls"
        )

    def __str__(self):
        return self.control_class + " " + self.control_id + " " + self.title

    def field_name_changes(self):
        d = {"id": "control_id", "class": "control_class", "controls": "control_enhancements"}
        return d


    def to_html(self):
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
                html_str = html_str.replace(str_to_replace, '(<i>' + coalesce(i.select,i.label,i.param_id) + '</i>)')
            # html_str += "<h5>Parameters:</h5>"
            # html_str += "<p><table border=1><tr align='center'>"
            # html_str += "<th>param_id</th><th>depends_on</th><th>label</th><th>usage</th><th>values</th><th>select</th><th>how_many</th><th>choice</th>"
            # for i in self.params.all():
            #     html_str += "<tr>"
            #     html_str += i.to_html()
            #     html_str += "</tr>"
            # html_str += "</table></p>"
        if self.links is not None:
            related_to_links = []
            for i in self.links.filter(rel="related"):
                related_to_links.append("<a href='" + i.href + "'>" + i.href[1:].upper() + "</a>")
            html_str += "<p><strong>Related Controls:</strong> "
            html_str += ", ".join(related_to_links)
            html_str += "</p>"

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


class groups(PrimitiveModel):
    """
    A Group is an arbitrary collection of controls.  It cna contain other groups and controls
    """

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"

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
    params = CustomManyToManyField(
        to=params, verbose_name="Global Group Parameters",
        help_text="Parameters that should be applied to all Controls in the Group"
        )
    props = propertiesField(
        verbose_name="Global Group Properties",
        help_text="Properties that should be applied to all Controls in the Group"
        )
    links = CustomManyToManyField(to=links, verbose_name="Links")
    parts = CustomManyToManyField(
        to=parts, verbose_name="Parts",
        help_text="A partition of a control's definition or a child of another part."
        )
    sub_groups = CustomManyToManyField(
        to="groups", verbose_name="Sub Groups",
        help_text="A group of controls, or of groups of controls."
        )
    controls = CustomManyToManyField(
        to="controls", verbose_name="Controls",
        help_text="A structured information object representing a security or privacy control. Each security or privacy control within the Catalog is defined by a distinct control instance."
        )

    def __str__(self):
        return self.group_id.upper() + " - " + self.title + " (" + self.group_class + ")"

    def field_name_changes(self):
        d = {"id": "group_id", "class": "group_class", "groups": "sub_groups"}
        return d

    def to_html(self):
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


class catalogs(PrimitiveModel):
    """
    A collection of controls.
    """

    class Meta:
        verbose_name = "Control Catalog"
        verbose_name_plural = "Control Catalogs"

    uuid = ShortTextField(verbose_name="Catalog Universally Unique Identifier")
    metadata = models.ForeignKey(
        to=metadata, verbose_name="Publication metadata",
        help_text="Provides information about the publication and availability of the containing document.",
        on_delete=models.CASCADE
        )
    params = CustomManyToManyField(
        to=params, verbose_name="Global Catalog Parameters",
        help_text="Parameters that should be applied to all Controls in the Catalog"
        )
    controls = CustomManyToManyField(to=controls, verbose_name="Controls")
    groups = CustomManyToManyField(to=groups, verbose_name="Groups")
    back_matter = models.ForeignKey(to=back_matter, verbose_name="Back Matter", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.metadata.title

    def get_absolute_url(self):
        return reverse('catalog:catalog_detail_view', kwargs={'pk': self.pk})

    def to_html(self):
        html_str = "<h1>" + self.metadata.title + "</h1>"
        html_str += "<h2>Metadata</h2>"
        html_str += self.metadata.to_html()
        html_str += "<hr>\n"
        if self.params is not None:
            html_str += "<h1>Global Paramaters</h1>\n"
            for i in self.params.all():
                html_str += i.to_html()
        if self.groups is not None:
            html_str += "<h1>Groups</h1>\n"
            for i in self.groups.all():
                html_str += i.to_html()
        if self.controls is not None:
            html_str += "<h1>Controls not in a Group</h1>\n"
            for i in self.controls.all():
                html_str += i.to_html()
        if self.back_matter is not None:
            html_str += "<h1>CBack Matter</h1>\n"
            html_str += self.back_matter.to_html()
        return html_str
