from common.models import *
from catalog.models import controls, params, catalogs
import re


# Create your models here.


class imports(BasicModel):
    """
    the import designates a catalog, profile, or other resource to be included (referenced and potentially modified) by this profile. The import also identifies which controls to select using the include-all, include-controls, and exclude-controls directives.
    Note that the OSCAL model allows including or excluding controls by pattern. This is not supported in OPAL.
    """

    class Meta:
        verbose_name = "Import"
        verbose_name_plural = "Imports"

    href = ShortTextField(
        verbose_name="Link to catalog or profiles", help_text="URI to access the catalog or profiles to be imported"
        )
    import_type = ShortTextField(
        verbose_name="Type of Import", choices=[("catalog", "Catalog"), ("profiles", "Profile")],
        help_text="Select if this import is for a catalog or a profiles"
        )
    include_all = models.BooleanField(
        verbose_name="Include all controls",
        help_text="Select this option to include all controls from the imported catalog or profiles", default=True
        )
    include_controls = CustomManyToManyField(
        to=controls, verbose_name="Included Controls",
        help_text="Select the controls to be included. Any controls not explicitly selected will be excluded",
        related_name="include_controls"
        )
    exclude_controls = CustomManyToManyField(
        to=controls, verbose_name="Excluded Controls",
        help_text="Select the controls to be excluded. Any controls not explicitly selected will be excluded",
        related_name="exclude_controls"
        )

    def __str__(self):
        return self.href

    def to_html(self):
        html_str = "<a href='" + self.href + "'>"
        if self.include_all:
            html_str += "Include all controls from " + self.import_type + " " + self.href
        elif len(self.include_controls.all()) > 0:
            ctr_list = []
            for c in self.include_controls.all():
                ctr_list.append(c)
            html_str += "Include only the following controls from " + self.import_type + " " + self.href + ".<br>"
            html_str += ", ".join(ctr_list)
        elif len(self.exclude_controls.all()) > 0:
            ctr_list = []
            for c in self.include_controls.all():
                ctr_list.append(c)
            html_str += "Include all controls from " + self.import_type + " " + self.href + " except the following.<br>"
            html_str += ", ".join(ctr_list)
        html_str += "</a>"
        return html_str


class modify(BasicModel):
    """
    Set parameters or amend controls in resolution
    """

    class Meta:
        verbose_name = "Modify Controls"
        verbose_name_plural = "Modify Controls"

    set_parameters = CustomManyToManyField(
        to=params, verbose_name="Modified Paramaters", help_text="Select any parameters you wish to modify"
        )
    alters = CustomManyToManyField(
        to=controls, verbose_name="Modified Controls", help_text="Select any controls you wish to modify"
        )


merge_options = [("use-first",
                  "Use the first definition - the first control with a given ID is used; subsequent ones are discarded"),
                 ("keep", "Keep - controls with the same ID are kept, retaining the clash")]


class profiles(BasicModel):
    """
    An OSCAL document that describes a tailoring of controls from one or more catalogs, with possible modification of multiple controls.
    """

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    metadata = models.ForeignKey(to=metadata, on_delete=models.CASCADE)
    imports = CustomManyToManyField(
        to=imports, verbose_name="Imports",
        help_text="The import designates a catalog, profiles, or other resource to be included (referenced and potentially modified) by this profiles. The import also identifies which controls to select using the include-all, include-controls, and exclude-controls directives."
        )
    merge = ShortTextField(
        verbose_name="Merge Strategy",
        help_text="A Merge element provides structuring directives that drive how controls are organized after resolution.",
        null=True, choices=merge_options
        )
    modify = models.ForeignKey(
        to=modify, verbose_name="Modifications",
        help_text="Define paramaters and controls that are modified by this profiles.", on_delete=models.CASCADE,
        null=True
        )
    # TODO: We need to create a function that will make a copy of existing paramaters/controls selected for modification
    back_matter = models.ForeignKey(
        to=back_matter, verbose_name="Back matter",
        help_text="Provides a collection of identified resource objects that can be referenced by a link with a rel value of 'reference' and an href value that is a fragment '#' followed by a reference to a reference identifier. Other specialized link 'rel' values also use this pattern when indicated in that context of use.",
        on_delete=models.CASCADE, null=True
        )

    def __str__(self):
        return self.metadata.title

    def get_absolute_url(self):
        return reverse('ctrl_profile:profile_detail_view', kwargs={'pk': self.pk})

    def list_all_controls(self):
        control_list = []
        regexp = re.compile('.*/common/p/')
        for ctrl in self.imports.all():
            re.match(regexp, ctrl.href)
            m = re.match(regexp, ctrl.href)
            if m is not None:
                obj = search_for_uuid(ctrl.href[m.end():])
                if obj is not None:
                    control_list.extend(obj.list_all_controls())
        return control_list


    def to_html(self):
        html_str = self.metadata.to_html()
        # Checking to see if the import is local
        regexp = re.compile('.*/common/p/')
        for ctrl in self.imports.all():
            re.match(regexp, ctrl.href)
            m = re.match(regexp, ctrl.href)
            if m is not None:
                obj_uuid = ctrl.href[m.end():]
                if obj_uuid is not None and catalogs.objects.filter(uuid=obj_uuid).exists():
                    obj = catalogs.objects.get(uuid=obj_uuid)
                    html_str = "<h1>" + obj.metadata.title + "</h1>"
                    html_str += "<h2>Metadata</h2>"
                    html_str += obj.metadata.to_html()
                    html_str += "<hr>\n"
                    html_str += "<table class='table table-striped'>\n"
                    if obj.groups is not None:
                        for group in obj.groups.all():
                            html_str += "<tr><td colspan=3><h3>" + group.__str__() + "</h3></td></tr>"
                            if group.sub_groups is not None:
                                for sub_group in group.sub_groups.all():
                                    html_str += "<tr><td colspan=3><h4>" + sub_group.__str__() + "</h4></td></tr>"
                            if group.controls is not None:
                                for ctrl in group.controls.all():
                                    html_str += "<tr>"
                                    html_str += "<th>" + ctrl.__str__() + "</th>"
                                    html_str += "<td>Implemented By: %s</td>" % ctrl.get_all_components()
                                    html_str += "<td></td>"
                                    html_str += "</tr>"
                    if obj.controls is not None:
                        html_str += "<tr><td colspan=3><h3>Controls not in a Group</h3></td></tr>"
                        for ctrl in obj.controls.all():
                            html_str += "<tr>"
                            html_str += "<th>" + ctrl.__str__() + "</th>"
                            html_str += "<td><a href='" + reverse(
                                'component:new_requirement', kwargs={'control_id': ctrl.id}
                                ) + "'>Define</a></td>"
                            html_str += "<td><a href=''>Modify</a></td>"
                            html_str += "</tr>"
                    html_str += "</table>\n"
        return html_str
