import ssp.models
from ssp.models.users import *


def run():
    #Using Dictionary property
    #print(nist_control_parameter().get_dictionary_json)

    #Creating JSON for person model pk=1
    print("---- Person model JSON ----")
    print(person().get_serializer_json(1))

