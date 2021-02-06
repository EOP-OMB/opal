from ssp.models.users import *
from opal.settings import IMPORTED_CATALOGS_DIR
import json
from django.utils.html import mark_safe

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
    param_text = models.CharField(max_length=1024, blank=True)
    param_depends_on = models.CharField(max_length=255, blank=True)
    param_class = models.CharField(max_length=255, blank=True)
    nist_control = models.ForeignKey('nist_control', on_delete=models.CASCADE)

    def __str__(self):
        return self.param_id

    #Sample JSON export using dictionary -- will be removed later
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
                d = {}
                for kv in key_value_list:
                    if kv[0] == 'uuid':
                        d[kv[0]] = str(getattr(obj, kv[
                            1]))  # Had to add this line to fix the UUID error when converting the list to json
                    else:
                        d[kv[0]] = getattr(obj, kv[1])
                return_list.append(d)
            json_str = json.dumps(return_list, indent=2)
            return json_str

    @staticmethod
    def get_serializer_json(id=1):
        queryset = nist_control_parameter.objects.filter(pk=id)
        serializer = nist_control_parameter_serializer(queryset, many=True)
        return (serializerJSON(serializer.data))


class nist_control_statement(PrimitiveModel):
    # control_id = models.CharField(max_length=50)
    nist_control = models.ForeignKey('nist_control', on_delete=models.CASCADE)
    statement_type = models.CharField(max_length=255)
    statement_text = customTextField()

    def __str__(self):
        return self.nist_control.label + ' - ' + self.statement_type.capitalize()

    @staticmethod
    def get_serializer_json(id=1):
        queryset = nist_control_statement.objects.filter(pk=id)
        serializer = nist_control_statement_serializer(queryset, many=True)
        return (serializerJSON(serializer.data))


class nist_control(PrimitiveModel):
    group_id = models.CharField(max_length=50)
    group_title = models.CharField(max_length=255)
    control_id = models.CharField(max_length=50)
    source = models.CharField(max_length=50)
    control_title = models.CharField(max_length=255)
    label = models.CharField(max_length=50)
    sort_id = models.CharField(max_length=50)
    status = models.CharField(max_length=255, blank=True)
    links = customMany2ManyField(link)
    catalog = models.CharField(max_length=50, null=True)

    class Meta:
        ordering = ['sort_id', 'catalog', 'control_title']

    def getStatementText(self, statement_type):
        t = nist_control_statement.objects.filter(nist_control=self,
                                                  statement_type=statement_type).get().statement_text
        for obj in self.parameters.all():
            t = t.replace('{{ ' + obj.param_id + ' }}', '(<i>' + obj.param_text + '</i>)')
        return t

    @property
    def get_guidance(self):
        return self.getStatementText('guidance')

    @property
    def get_statement(self):
        return self.getStatementText('statement')

    @property
    def parameters(self):
        return nist_control_parameter.objects.filter(nist_control=self)

    @property
    def long_title(self):
        long_title = self.group_title + ' | ' + self.label + ' | ' + self.control_title
        return long_title

    # TODO: Add methods for objectives and whatever the other type is

    @property
    def all_text(self):
        html = "<b>" + self.long_title + "</b>"
        html = html + "<p>" + self.get_statement + "</p>"
        return mark_safe(html)

    def __str__(self):
        return '(' + self.catalog + ')' + self.long_title

    @staticmethod
    def get_serializer_json(id=1):
        queryset = nist_control.objects.filter(pk=id)
        serializer = nist_control_serializer(queryset, many=True)
        return (serializerJSON(serializer.data))


class control_baseline(BasicModel):
    controls = customMany2ManyField(nist_control)
    link = models.ForeignKey(link, on_delete=models.PROTECT, null=True, blank=True, related_name='control_baseline_set')

    @staticmethod
    def get_serializer_json(id=1):
        queryset = control_baseline.objects.filter(pk=id)
        serializer = control_baseline_serializer(queryset, many=True)
        return (serializerJSON(serializer.data))



class control_statement(ExtendedBasicModel):
    """
    responses to the requirements defined in each control.  control_statement_id should be
    in the format 'Part a.'.
    """

    class Meta:
        ordering = ["short_name"]

    control_statement_id = models.CharField(max_length=25)
    control_statement_responsible_roles = customMany2ManyField(user_role)
    control_statement_text = customTextField()

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.id is not None and self.system_control_set.count() > 0:
            self.title = ' - '.join([self.system_control_set.first().control_primary_system.short_name,
                                     self.system_control_set.first().title, self.control_statement_id])
            self.short_name = '-'.join([self.system_control_set.first().control_primary_system.short_name,
                                        self.system_control_set.first().short_name, self.control_statement_id])
        else:
            self.title = ' - '.join(['UNLINKED', self.control_statement_id])
            self.short_name = '-'.join(['UNLINKED', self.control_statement_id])
        super(control_statement, self).save(force_insert, force_update)

    @property
    def nist_control_text(self):
        return self.system_control_set.first().nist_control.all_text

    @staticmethod
    def get_serializer_json(id=1):
        queryset = control_statement.objects.filter(pk=id)
        serializer = control_statement_serializer(queryset, many=True)
        return (serializerJSON(serializer.data))


class control_parameter(BasicModel):
    class Meta:
        ordering = ["short_name","control_parameter_id"]

    control_parameter_id = models.CharField(max_length=25)
    value = customTextField()

    def save(self, force_insert=False, force_update=False):
        if self.id is not None and self.system_control_set.count() > 0:
            self.title = ' - '.join([self.system_control_set.first().control_primary_system.short_name,
                                     self.system_control_set.first().title, self.control_parameter_id])
            self.short_name = '-'.join([self.system_control_set.first().control_primary_system.short_name,
                                        self.system_control_set.first().short_name, self.control_parameter_id])
        else:
            self.title = ' - '.join(['UNLINKED', self.control_parameter_id])
            self.short_name = '-'.join(['UNLINKED', self.control_parameter_id])
        super(control_parameter, self).save(force_insert, force_update)

    @staticmethod
    def get_serializer_json(id=1):
        queryset = control_parameter.objects.filter(pk=id)
        serializer = control_parameter_serializer(queryset, many=True)
        return (serializerJSON(serializer.data))



control_implementation_status_choices = [
    ('Implemented', 'Implemented'),
    ('Parti1ally Implemented ', 'Partially Implemented'),
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
    control_primary_system = models.ForeignKey('system_security_plan', on_delete=models.DO_NOTHING, null=True)
    nist_control = models.ForeignKey(nist_control, on_delete=models.DO_NOTHING, null=True,
                                     related_name='system_control_set')

    class Meta:
        ordering = ['nist_control']

    @property
    def sorted_statement_set(self):
        return self.control_statements.order_by('control_statement_id')

    @property
    def nist_control_text(self):
        return self.nist_control.all_text

    @property
    def system_security_plan_title(self):
        return self.system_security_plan_set.values()[0]["title"]

    @staticmethod
    def get_serializer_json(id=1):
        queryset = system_control.objects.filter(pk=id)
        serializer = system_control_serializer(queryset, many=True)
        return (serializerJSON(serializer.data))



frequency_choices = [('daily', 'Daily'),
                    ('weekly', 'weekly'),
                    ('monthly', 'Monthly'),
                    ('quarterly', 'Quarterly'),
                    ('annually', 'Annually'),
                    ('as needed', 'As Needed')]

class continuous_monitoring_action_item(BasicModel):
    control_statements = customMany2ManyField(control_statement)
    automated = models.BooleanField(default=True)
    frequency = models.CharField(max_length=10, choices=frequency_choices, default='as needed')



class import_catalog(PrimitiveModel):
    title = models.CharField(max_length=255, blank=True, null=True)
    file_url = models.URLField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to=IMPORTED_CATALOGS_DIR, blank=True, null=True)
    control_baseline = models.ForeignKey(control_baseline, on_delete=models.DO_NOTHING, null=True, blank=True,
                                     related_name='import_catalog_set')
    added_controls = models.IntegerField(blank=True, null=True)
    updated_controls = models.IntegerField(blank=True, null=True)
    user = models.CharField(max_length=255, blank=True, null=True)




"""
***********************************************************
******************  Serializer Classes  *******************
***********************************************************
"""


class nist_control_parameter_serializer(serializers.ModelSerializer):
    class Meta:
        model = nist_control_parameter
        fields = ['id', 'uuid', 'param_id', 'param_type', 'param_text', 'param_depends_on', 'param_class']


class nist_control_statement_serializer(serializers.ModelSerializer):
    class Meta:
        model = nist_control_statement
        fields = ['id', 'uuid', 'statement_type', 'statement_text', 'nist_control_id']
        depth = 1


class control_statement_serializer(serializers.ModelSerializer):
    control_statement_responsible_roles = user_role_serializer(many=True, read_only=True)

    class Meta:
        model = control_statement
        fields = ['id', 'uuid', 'title', 'short-name', 'description', 'remarks', 'properties', 'annotations', 'links',
                  'control_statement_id', 'control_statement_responsible_roles', 'control_statement_text']

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }


class control_parameter_serializer(serializers.ModelSerializer):
    class Meta:
        model = control_parameter
        fields = ['id', 'uuid', 'title', 'short-name', 'description', 'remarks', 'control_parameter_id', 'value']

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }


class system_control_serializer(serializers.ModelSerializer):
    control_parameters = control_parameter_serializer(many=True, read_only=True)
    control_statements = control_statement_serializer(many=True, read_only=True)

    class Meta:
        model = system_control
        fields = ['id', 'uuid', 'title', 'short-name', 'description', 'remarks', 'properties', 'annotations', 'links',
                  'control_parameters', 'control_statements', 'control_status', 'control_origination',
                  'nist_control_id']
        depth = 1

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }


class nist_control_serializer(serializers.ModelSerializer):
    parameters = nist_control_parameter_serializer(many=True, read_only=True)
    links = link_serializer(many=True, read_only=True)
    system_control_set = system_control_serializer(many=True, read_only=True)
    nist_control_statement_set = nist_control_statement_serializer(many=True, read_only=True)

    class Meta:
        model = nist_control
        fields = ['id', 'uuid', 'group_id', 'group_title', 'control_id', 'source', 'control_title',
                  'label', 'sort_id', 'status', 'catalog', 'parameters', 'links', 'system_control_set',
                  'nist_control_statement_set']

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }


class control_baseline_serializer(serializers.ModelSerializer):
    controls = nist_control_serializer(many=True, read_only=True)
    link = link_serializer(many=False, read_only=True)

    class Meta:
        model = control_baseline
        fields = ['id', 'uuid', 'title', 'short-name', 'description', 'remarks', 'controls', 'link']

        extra_kwargs = {
            'short-name': {'source': 'short_name'},
            'description': {'source': 'desc'}
        }
        depth = 1


class link_serializer(serializers.ModelSerializer):
    hash = hashed_value_serializer(many=False, read_only=True)
    control_baseline_set = control_baseline_serializer(many=True, read_only=True)

    class Meta:
        model = link
        fields = ['id', 'uuid', 'text', 'href', 'requires_authentication', 'rel', 'mediaType', 'hash',
                  'control_baseline_set']
        depth = 1