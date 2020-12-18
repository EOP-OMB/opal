from ssp.models.systems import *
from opal.settings import BASE_DIR

def run():
    #Using Dictionary property
    #print(nist_control_parameter().get_dictionary_json)

    #print(system_security_plan().get_serializer_json(2))
    f = open(BASE_DIR + '/opal.json', "w")
    f.write(system_security_plan().get_serializer_json(1))
    f.close()
    print("JSON file is created")

