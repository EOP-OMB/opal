import json

from catalog.models import *

"""
Some useful common functions
"""


def import_catalog(catalog_file="sample_data/basic-catalog.json"):
    catalog_json = json.load(open(catalog_file))
    catalog_dict = catalog_json["catalog"]
    new_catalog = catalogs()
    new_catalog.import_oscal(catalog_dict)
    new_catalog.save()
    return new_catalog

def import_all_catalogs():
    import requests
    from common.functions import reset_all_db
    from common.views import available_catalog_list
    reset_all_db()
    import json
    from catalog.models import catalogs
    for item in available_catalog_list:
        catalog_url = item["link"]
        f = requests.get(catalog_url)
        catalog_json = json.loads(f.text)
        catalog_dict = catalog_json["catalog"]
        new_catalog = catalogs()
        new_catalog.import_oscal(catalog_dict)
        new_catalog.save()