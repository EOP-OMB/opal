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
