import logging
from uuid import UUID
from django.apps import apps
from django.core.exceptions import FieldError

"""
Some useful common functions
"""

from opal.settings import USER_APPS


def replace_hyphen(s: str):
    logger = logging.getLogger("django")
    logger.info("replacing hyphen in " + s + " with underscore.")
    return s.replace("-", "_")


def reset_db(app_name):
    logger = logging.getLogger("django")
    app_models = apps.get_app_config(app_name).get_models()
    logger.info("Deleting all records from app " + app_name)
    for model in app_models:
        logger.info("Deleting " + str(model.objects.count()) + " items from " + model._meta.model_name)
        model.objects.all().delete()
        logger.info("Done. " + str(model.objects.count()) + " items remain in " + model._meta.model_name)


def reset_all_db():
    for app in USER_APPS:
        reset_db(app)


# got this from https://towardsdatascience.com/4-cute-python-functions-for-working-with-dirty-data-2cf7974280b5
def coalesce(*values):
    """Return the first non-None value or None if all values are None"""
    return next((v for v in values if v is not None and v != ""), "N/A")


from django.core.exceptions import ObjectDoesNotExist


def search_for_uuid(uuid_str, app_list=USER_APPS):
    logger = logging.getLogger("django")
    try:
        logger.info("Searching for uuid: " + uuid_str)
        uuid_obj = UUID(uuid_str, version=4)
        # r = None
        for a in app_list:
            logger.info("Looking in app " + a.title())
            app_models = apps.get_app_config(a).get_models()
            logger.info("Got list of models")
            for model in app_models:
                logger.info("Trying " + model._meta.model_name)
                try:
                    r = model.objects.get(uuid=uuid_str)
                    logging.debug("Found matching!")
                    return r
                except ObjectDoesNotExist:
                    r = None
                except FieldError:
                    # uuid field does not exist
                    r = None
        logger.info("Could not find an object with uuid: " + uuid_str)
        return None
    except ValueError:
        logger.info(uuid_str + " is not a valid uuid")
        return None
