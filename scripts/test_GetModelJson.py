from ssp.serializers import *
from ssp.models import *
from rest_framework.renderers import JSONRenderer
import json


def run():
    #Using Django Core serializer
    #print(nist_control_parameter().get_serializer_json)

    #Using Dictionary property
    #print(nist_control_parameter().get_dictionary_json)

    #Creating JSON for person model all data
    print("---- person model JSON ----")
    queryset = person.objects.all()
    serializer = person_serializer(queryset, many=True)
    data = serializer.data
    json_data = JSONRenderer().render(data)
    json_object = json.loads(json_data)
    json_str = json.dumps(json_object, indent=2)
    print(json_str)

