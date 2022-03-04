import logging
from django.apps import apps



"""
Some useful common functions
"""

import logging.handlers
import os
from opal.settings import USER_APPS

# your logging setup

def start_logging():
    log_filename = "opal_debug.log"
    # should_roll_over = os.path.isfile(log_filename)
    # handler = logging.handlers.RotatingFileHandler(log_filename, mode='w', backupCount=5)
    # if should_roll_over:  # log already exists, roll over!
    #     handler.doRollover()
    logging.basicConfig(
        filename=log_filename,
        format='%(asctime)s %(name)-12s %(pathname)s:%(lineno)d %(levelname)-8s %(message)s',
        filemode='w'
        )
    logger = logging.getLogger()
    logger.setLevel("DEBUG")
    return logger

def replace_hyphen(s: str):
    logger = logging.getLogger("file")
    logger.debug("replacing hyphen in " + s + " with underscore.")
    return s.replace("-", "_")


def reset_db(app_name):
    logger = start_logging()
    app_models = apps.get_app_config(app_name).get_models()
    logger.info("Deleting all records from app " + app_name)
    for model in app_models:
        logger.debug("Deleting " + str(model.objects.count()) + " items from " + model._meta.model_name)
        model.objects.all().delete()
        logger.debug("Done. " + str(model.objects.count()) + " items remain in " + model._meta.model_name)

def reset_all_db():
    for app in USER_APPS:
        reset_db(app)


# got this from https://towardsdatascience.com/4-cute-python-functions-for-working-with-dirty-data-2cf7974280b5
def coalesce(*values):
    """Return the first non-None value or None if all values are None"""
    return next((v for v in values if v is not None and v != ""), "N/A")

from django.core.exceptions import ObjectDoesNotExist

def search_for_uuid(uuid_str,app_list=USER_APPS):
    logger = start_logging()
    logger.debug("Looking for uuid " + uuid_str)
    r = None
    for a in app_list:
        logger.debug("searching app " + a)
        app_models = apps.get_app_config(a).get_models()
        for model in app_models:
            for field in model._meta.concrete_fields:
                if field.name == "uuid":
                    logger.debug("Searching model " + model._meta.model_name)
                    try:
                        r = model.objects.get(uuid=uuid_str)
                        return r
                    except ObjectDoesNotExist:
                        r = None
    return r
