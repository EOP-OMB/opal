from common.models import *
from catalog.models import controls, params


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
        verbose_name="Link to catalog or profile", help_text="URI to access the catalog or profile to be imported"
        )
    import_type = ShortTextField(verbose_name="Type of Import",choices=[("catalog","Catalog"),("profile","Profile")],help_text="Select if this import is for a catalog or a profile")
    include_all = models.BooleanField(
        verbose_name="Include all controls",
        help_text="Select this option to include all controls from the imported catalog or profile", default=True
        )
    include_controls = CustomManyToManyField(
        controls, verbose_name="Included Controls",
        help_text="Select the controls to be included. Any controls not explicitly selected will be excluded",related_name="include_controls"
        )
    exclude_controls = CustomManyToManyField(
        controls, verbose_name="Excluded Controls",
        help_text="Select the controls to be excluded. Any controls not explicitly selected will be excluded",related_name="exclude_controls"
        )

    def __str__(self):
        return self.href

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


class profile(BasicModel):
    """
    An OSCAL document that describes a tailoring of controls from one or more catalogs, with possible modification of multiple controls.
    """

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    metadata = models.ForeignKey(to=metadata, on_delete=models.CASCADE)
    imports = CustomManyToManyField(
        to=imports, verbose_name="Imports",
        help_text="The import designates a catalog, profile, or other resource to be included (referenced and potentially modified) by this profile. The import also identifies which controls to select using the include-all, include-controls, and exclude-controls directives."
        )
    merge = ShortTextField(verbose_name="Merge Strategy",
        help_text="A Merge element provides structuring directives that drive how controls are organized after resolution.",null=True,choices=merge_options
        )
    modify = models.ForeignKey(
        to=modify, verbose_name="Modifications",
        help_text="Define paramaters and controls that are modified by this profile.", on_delete=models.CASCADE, null=True
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
        # TODO - this function should return some kind of permalink using the uuid
        return reverse('control_profile:profile_detail_view', kwargs={'pk': self.pk})
