from ssp.models.systems import *
from opal.settings import BASE_DIR

def run():
    #Using Dictionary property
    #print(nist_control_parameter().get_dictionary_json)

    #queryset = inventory_item_type.objects.filter(pk=1)
    #serializer = inventory_item_type_serializer(queryset, many=True)
    #print(serializerJSON(serializer.data))

    f = open(BASE_DIR + '/opal.json', "w")
    f.write(system_security_plan().get_serializer_json_OSCAL(1))
    f.close()
    print("JSON file is created")

