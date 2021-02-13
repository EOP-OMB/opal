from ssp.models.systems import *
from opal.settings import BASE_DIR

def run():
    #Using Dictionary property
    #print(nist_control_parameter().get_dictionary_json)

    queryset = system_interconnection.objects.filter(pk=2)
    serializer = system_interconnection_serializer(queryset, many=True)
    print(serializerJSON(serializer.data))

    """f = open(BASE_DIR + '/opal.json', "w")
    f.write(control_baseline().get_serializer_json(1))
    f.close()
    print("JSON file is created")"""

