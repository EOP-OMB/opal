from django import forms

from catalog.models import catalogs, controls
from component.models import by_components, components
from common.models import roles


class select_control_statements_form(forms.Form):
    catalogs = forms.ModelChoiceField(queryset=catalogs.objects.all())
    controls = forms.ModelChoiceField(queryset=controls.objects.all())
    statements = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[]
        )


class component_statement_form(forms.Form):
    component_uuid = forms.ModelChoiceField(queryset=components.objects.all())
    implementation_status = forms.ChoiceField(choices=by_components.implementation_status.field.choices)
    responsible_roles = forms.ModelMultipleChoiceField(queryset=roles.objects.all())
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 60}))


from django.forms import inlineformset_factory, Textarea
from component.models import components, control_implementations, implemented_requirements, by_components, statements, parameters


class componentForm(forms.ModelForm):
    class Meta:
        model = components
        fields = ('title', 'type', 'description', 'purpose', 'status')


class control_implementationForm(forms.ModelForm):
    class Meta:
        model = control_implementations
        fields = ('description',)


control_implementationInlineFormset = inlineformset_factory(
    components,
    control_implementations,
    form=control_implementationForm,
    widgets=({'description': Textarea(attrs={'cols': 80, 'rows': 20})}),
    extra=3
    )


class implemented_requirementForm(forms.ModelForm):
    class Meta:
        model = implemented_requirements
        fields = ('control_id',)


implemented_requirementInlineFormset = inlineformset_factory(
    control_implementations,
    implemented_requirements,
    form=implemented_requirementForm,
    extra=1
    )


class statementForm(forms.ModelForm):
    class Meta:
        model = statements
        fields = ('statement_id',)


statementInlineFormset = inlineformset_factory(
    implemented_requirements,
    statements,
    form=statementForm,
    extra=1
    )


class by_componentForm(forms.ModelForm):
    class Meta:
        model = by_components
        fields = ('component_uuid', 'description', 'implementation_status', 'set_parameters')


by_componentInlineFormset = inlineformset_factory(
    implemented_requirements,
    by_components,
    form=by_componentForm,
    extra=1
    )


class parameterForm(forms.ModelForm):
    class Meta:
        model = parameters
        fields = ('param_id', 'values')


parameterInlineFormset = inlineformset_factory(
    by_components,
    parameters,
    form=parameterForm,
    extra=1
    )

# control_implementationInlineFormset = inlineformset_factory(
#     components,
#     control_implementations,
#     form=control_implementationsForm,
#     extra=1,
# max_num=5,
# fk_name=None,
# fields=None, exclude=None, can_order=False,
# can_delete=True, max_num=None, formfield_callback=None,
# widgets=None, validate_max=False, localized_fields=None,
# labels=None, help_texts=None, error_messages=None,
# min_num=None, validate_min=False, field_classes=None
# )
