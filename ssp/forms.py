from django import forms
from django.forms import ModelForm
from ssp.models import system_security_plan, import_catalog, person, system_user
from scripts.usefullFunctions import validate_file_extension


class SystemSecurityPlan(ModelForm):
    class Meta:
        model = system_security_plan
        fields = '__all__'


class ImportCatalogForm(ModelForm):
    title = forms.CharField(label='Catalog Title', max_length=255, required=True)
    file = forms.FileField(label='Catalog File', max_length=255, required=False)
    file_url = forms.CharField(label='Catalog File URL', max_length=255, required=False)

    class Meta:
        model = import_catalog
        fields = ['title', 'file_url', 'file']

    def __init__(self, *args, **kwargs):
        super(ImportCatalogForm, self).__init__(*args, **kwargs)  # Call to ModelForm constructor
        self.fields['title'].widget.attrs['style'] = 'width:660px; height:30px;'
        self.fields['file_url'].widget.attrs['style'] = 'width:635px; height:30px;'

    def clean(self):
        super(ImportCatalogForm, self).clean()

        title = self.cleaned_data.get('title')
        file_url = self.cleaned_data.get('file_url')
        file = self.cleaned_data.get('file')

        if len(title) == 0 :
            self.add_error('title', "Title required") #field error
            #self._errors['title'] = self.error_class(['Title required']) #another way of adding field error
        if file:
            if not validate_file_extension(file.name, '.json'):
                self.add_error('file', 'URL for a Catalog file with JSON format required')
        if file_url:
            if not validate_file_extension(file_url, '.json'):
                self.add_error('file_url', 'Catalog file with JSON format required')
        if not file_url and not file:
            raise forms.ValidationError("Either a file or a URL required") #non_field error
        if file_url and file:
            raise forms.ValidationError("Only a file or a URL required") #non_field error

        return self.cleaned_data


class SystemUserNewForm(forms.Form):
    PEOPLE=[]
    for prsn in person.objects.all():
        prsn_id = prsn.pk
        prsn_display = 'Name: '+ prsn.name + ', Title: ' + prsn.title
        prsn_tuple = (prsn_id,prsn_display)
        PEOPLE.append(prsn_tuple)

    user = forms.CharField(label='User', max_length=255, required=True, widget=forms.Select(choices=PEOPLE))


    def __init__(self, *args, **kwargs):
        super(SystemUserNewForm, self).__init__(*args, **kwargs)  # Call to ModelForm constructor
        self.fields['user'].widget.attrs['style'] = 'width:660px; height:30px;'

    def clean(self):
        super(SystemUserNewForm, self).clean()

        user = self.cleaned_data.get('user')

        if len(user) == 0 :
            self.add_error('user', "User required") #field error

        return self.cleaned_data


