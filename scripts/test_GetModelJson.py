from ssp.serializers import *
from ssp.models import *
from rest_framework.renderers import JSONRenderer
import json


def run():
    # Please comment out one line at the time to see the result of each property
    #print(nist_control_parameter().get_serializer_json)
    #print(nist_control_parameter().get_dictionary_json)

    #queryset = nist_control_parameter.objects.all()
    queryset = nist_control_parameter.objects.filter(param_id="sr-8_prm_2")
    serializer = nist_control_parameter_serializer(queryset, many=True)
    data = serializer.data
    #return data["json"]
    json_data = JSONRenderer().render(data)
    json_object = json.loads(json_data)
    json_str = json.dumps(json_object, indent=2)
    print(json_str)