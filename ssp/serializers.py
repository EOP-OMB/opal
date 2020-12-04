from rest_framework_json_api import serializers
from ssp.models import nist_control_parameter


class nist_control_parameter_serializer(serializers.ModelSerializer):

    alias1 = serializers.CharField(source='param_id')

    class Meta:
        model = nist_control_parameter
        fields = ['alias1', 'param_type', 'param_text', 'param_depends_on','param_class']
        #fields = '__all__'