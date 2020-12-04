from ssp.models.users import *

#Samira:
from django.core import serializers
import json

# objects related to security controls

# Objects to hold control catalog data that should be displayed in the SSP

parameter_type_choices = [('label', 'Label'),
                          ('description', 'Description'),
                          ('constraint', 'Constraint'),
                          ('guidance', 'Guidance'),
                          ('value', 'Value'),
                          ('select', 'Select')]


class nist_control_parameter(PrimitiveModel):
    param_id = models.CharField(max_length=255)
    param_type = models.CharField(max_length=255, choices=parameter_type_choices)
    param_text = models.CharField(max_length=255, blank=True)
    param_depends_on = models.CharField(max_length=255, blank=True)
    param_class = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.param_id

#Samira:
    @property
    def get_serializer_json(self):
        if len(nist_control_parameter.objects.all()) == 0:
            return None
        else:
            json_data = serializers.serialize("json", nist_control_parameter.objects.all())
            # If you only want a subset of fields to be serialized, you can specify a fields argument to the serializer:
            # e.g. json_data = serializers.serialize("json", nist_control_parameter.objects.all(), fields=('uuid', 'param_id', 'param_type', 'param_text'))

            json_object = json.loads(json_data)
            json_str = json.dumps(json_object, indent=2)
            return json_str

    #Samira
    @property
    def get_dictionary_json(self):
        key_value_list = [
            ['id', 'pk'],
            ['uuid', 'uuid'],
            ['param_id', 'param_id'],
            ['param_type', 'param_type'],
            ['param_text', 'param_text'],
            ['param_depends_on', 'param_depends_on'],
            ['param_class', 'param_class']
        ]
        if len(nist_control_parameter.objects.all()) == 0:
            return None
        else:
            return_list = []
            for obj in nist_control_parameter.objects.all():
                dict = {}
                for kv in key_value_list:
                    if kv[0] == 'uuid':
                        dict[kv[0]]= str(getattr(obj, kv[1])) #Had to add this line to fix the UUID error when converting the list to json
                    else:
                        dict[kv[0]] = getattr(obj, kv[1])
                return_list.append(dict)
            json_str = json.dumps(return_list, indent=2)
            return json_str

class nist_control_statement(PrimitiveModel):
    # control_id = models.CharField(max_length=50)
    nist_control = models.ForeignKey('nist_control', on_delete=models.PROTECT, null=True)
    statement_type = models.CharField(max_length=255)
    statement_text = customTextField()

    def __str__(self):
        return self.nist_control.label + ' - ' + self.statement_type.capitalize()


class nist_control(PrimitiveModel):
    group_id = models.CharField(max_length=50)
    group_title = models.CharField(max_length=255)
    control_id = models.CharField(max_length=50, unique=True)
    source = models.CharField(max_length=50)
    control_title = models.CharField(max_length=255)
    label = models.CharField(max_length=50, unique=True)
    sort_id = models.CharField(max_length=50)
    status = models.CharField(max_length=255, blank=True)
    parameters = customMany2ManyField(nist_control_parameter)
    links = customMany2ManyField(link)


    def getStatementText(self, statement_type):
        t = nist_control_statement.objects.filter(nist_control=self,
                                                  statement_type=statement_type).get().statement_text
        for obj in self.parameters.all():
            t = t.replace('{{ ' + obj.param_id + ' }}','(<i>' + obj.param_text + '</i>)')
        return t

    @property
    def get_guidance(self):
        return self.getStatementText('guidance')

    @property
    def get_statement(self):
        return self.getStatementText('statement')

    # TODO: Add methods for objectives and whatever the other type is


    def __str__(self):
        long_title = self.group_title + ' | ' + self.label + ' | ' + self.control_title
        return long_title


class control_baseline(BasicModel):
    controls = customMany2ManyField(nist_control)


class control_statement(ExtendedBasicModel):
    """
    responses to the requirements defined in each control.  control_statement_id should be
    in the format 'Part a.'.
    """
    class Meta:
        ordering = ["title"]

    control_statement_id = models.CharField(max_length=25)
    control_statement_responsible_roles = customMany2ManyField(user_role)
    control_statement_text = customTextField()


class control_parameter(BasicModel):
    control_parameter_id = models.CharField(max_length=25)
    value = customTextField()


# class control_implementation(ExtendedBasicModel):
# control_id = models.CharField(max_length=25)
# control_responsible_roles = customMany2ManyField(user_role)
# control_parameters = customMany2ManyField(control_parameter)
# control_statements = customMany2ManyField(control_statement)
# nist_control = models.ForeignKey(nist_control, on_delete=models.DO_NOTHING, null=True, blank=True)


control_implementation_status_choices = [
    ('Implemented', 'Implemented'),
    ('Partially Implemented ', 'Partially Implemented'),
    ('Planned ', 'Planned'),
    ('Alternative Implementation', 'Alternative Implementation'),
    ('Not Applicable', 'Not Applicable'),
    ('Other than Implemented', 'Other than Implemented')]

control_origination_choices = [
    ('Service Provider Corporate ', 'Service Provider Corporate'),
    ('Service Provider System Specific ', 'Service Provider System Specific'),
    ('Service Provider Hybrid (Corporate and System Specific)', 'Service Provider Hybrid'),
    ('Configured by Customer (Customer System Specific) ', 'Configured by Customer'),
    ('Provided by Customer (Customer System Specific) ', 'Provided by Customer'),
    ('Shared (Service Provider and Customer Responsibility) ', 'Shared'),
    ('Inherited ', 'Inherited'),
    ('N/A', 'N/A')]


class system_control(ExtendedBasicModel):
    control_parameters = customMany2ManyField(control_parameter)
    control_statements = customMany2ManyField(control_statement)
    control_status = models.CharField(max_length=100, choices=control_implementation_status_choices)
    control_origination = models.CharField(max_length=100, choices=control_origination_choices)
    nist_control = models.ForeignKey(nist_control, on_delete=models.DO_NOTHING, null=True)

    @property
    def sorted_statement_set(self):
        return self.control_statements.order_by('control_statement_id')


